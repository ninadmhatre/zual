try:
    from builtins import str
except ImportError:
    pass

import logging
from urllib import parse
import sqlalchemy as sqla
import datetime
from libs.Utils import Utility


class BaseStorage(object):
    def get_all_stats(self, include_all):
        raise NotImplemented('Please Implement!')

    def update_count(self, page_id):
        raise NotImplemented('Please Implement!')

    def get_count(self, page_id):
        raise NotImplemented('Please Implement!')

    def remove_page(self, page_id):
        raise NotImplemented('Please Implement!')

    def add_page(self, page_id, title):
        raise NotImplemented('Please Implement!')

    def create_table(self):
        raise NotImplemented('Please Implement!')


class SqliteStorage(BaseStorage):
    """
    Create a database and implement the ``BaseStorage`` methods to store the
    information about pages and their view count!
    """
    _db = None
    _logger = logging.getLogger("page-view-count")
    _logger.setLevel(logging.DEBUG)

    def __init__(self, engine=None, metadata=None, db=None):
        if db:
            self._engine = db.engine
            self._metadata = db.metadata
        else:
            if not engine:
                raise ValueError('Both db and engine args cannot be none!!!')
            self._engine = engine
            self._metadata = metadata or sqla.MetaData()

        self._metadata.reflect(bind=self._engine)
        self.table_name = 'page_views'
        self._count_table = None
        self.create_table()

    @property
    def metadata(self):
        return self._metadata

    def add_page(self, page_id, title):
        success = True
        with self._engine.begin() as conn:
            try:
                add_post = self._count_table.insert()

                post_statement = add_post.values(
                    page_id=page_id, title=title,
                    count=1, deleted=0,
                    last_modified_date=datetime.datetime.utcnow()
                )
                post_result = conn.execute(post_statement)
            except Exception as e:
                self._logger.exception(str(e))
                success = False
        return success

    def get_count(self, page_id):
        r = None
        with self._engine.begin() as conn:
            try:
                post_statement = sqla.select([self._count_table]).where(
                    self._count_table.c.page_id == page_id
                )
                post_result = conn.execute(post_statement).fetchone()
                if post_result:
                    r = dict(post_id=post_result[0], title=post_result[1],
                             count=post_result[2], deleted=post_result[3],
                             last_modified_date=post_result[4])
            except Exception as e:
                self._logger.exception(str(e))
                r = None
        return r

    def get_all_stats(self, include_all=False):
        r = {}
        with self._engine.begin() as conn:
            if include_all:
                post_statement = sqla.select([self._count_table])
            else:
                post_statement = sqla.select([self._count_table]).where(
                    self._count_table.c.deleted != 1
                )

            try:
                result = conn.execute(post_statement)
                for row in result.fetchall():
                    r[row[0]] = dict(title=row[1],
                                     count=row[2], deleted=row[3],
                                     last_modified_date=row[4])
            except Exception as e:
                self._logger.exception(str(e))
                r = None
        return r

    def update_count(self, page_id):
        success = True
        with self._engine.begin() as conn:
            try:
                post_statement = self._count_table.update().\
                    where(self._count_table.c.page_id == page_id).\
                    values(count=self._count_table.c.count + 1)
                result = conn.execute(post_statement)
            except Exception as e:
                self._logger.exception(str(e))
                success = False

        return success

    def remove_page(self, page_id):
        success = True
        with self._engine.begin() as conn:
            try:
                post_statement = self._count_table.update().\
                    where(self._count_table.c.page_id == page_id).\
                    values(deleted=1)
                result = conn.execute(post_statement)
            except Exception as e:
                self._logger.exception(str(e))
                success = False

        return success

    def create_table(self):
        with self._engine.begin() as conn:
            if not conn.dialect.has_table(conn, self.table_name):
                self._count_table = sqla.Table(
                    self.table_name, self._metadata,
                    sqla.Column("page_id", sqla.String(256), primary_key=True),
                    sqla.Column("title", sqla.String(512)),
                    sqla.Column("count", sqla.Integer, default=0),
                    sqla.Column("deleted", sqla.SmallInteger, default=0),
                    sqla.Column("last_modified_date", sqla.DateTime)
                )
                self._logger.debug("Created table with table name %s" %
                                   self.table_name)
            else:
                self._count_table = self._metadata.tables[self.table_name]
                self._logger.debug("Reflecting to table with table name %s" %
                                   self.table_name)


class Informer(object):
    def __init__(self, db):
        self.db = db
        self.cache = None
        self.refresh = True
        self._update_cache()

    def _encode_title(self, page_title):
        return parse.quote(page_title)

    def _decode_title(self, encoded_title):
        return parse.unquote(encoded_title)

    def _update_cache(self):
        self.cache = self.list()
        self.refresh = False

    def insert(self, page_id, page_title):
        if not page_id:
            page_id = Utility.get_md5_hash_of_title(page_title)

        if self.is_existing_page(page_id):
            return self.update(page_id)
        else:
            return self.db.add_page(page_id, page_title)

    def is_existing_page(self, page_id):
        return page_id in self.cache

    def update(self, page_title, is_page_id=False):
        if not is_page_id:
            page_id = Utility.get_md5_hash_of_title(page_title)
        else:
            page_id = page_title

        return self.db.update_count(page_id)

    def list(self, include_all=False):
        return self.db.get_all_stats(include_all=include_all)

    def get_count(self, page_id):
        return self.db.get_count(page_id)