__author__ = 'ninad mhatre'

from addonpy.IAddonInfo import IAddonInfo
from libs.AddonReturnType import AddonReturnType
from jinja2 import Template
from application import page_view_stats


class ViewStatsAddon(IAddonInfo, AddonReturnType):
    result = None
    status = True  # Data received properly

    def template(self):
        if self.result:
            html = '''<div class="col-lg-12"><div class="panel panel-success">
                <div class="panel-heading">
                    <h3 class="panel-title">
                        {{- name -}}
                        <span class="pull-right glyphicon glyphicon-thumbs-up"></span>
                    </h3>
                </div>
                <div id="counter" class="panel-collapse">
                    <div class="panel-body">
                        <table class="table table-bordered table-responsive">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Title</th>
                                    <th>Views</th>
                                    <th>Deleted?</th>
                                    <th>Last Viewed On</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for k in data %}
                                    <tr>
                                        <td>{{ k }}</td>
                                        <td>{{ data[k]['title']|toAscii }}</td>
                                        <td>{{ data[k]['count'] }}</td>
                                        <td>{{ data[k]['deleted']|toBoolean }}</td>
                                        <td>{{ data[k]['last_modified_date'] }}</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    <div class="panel-footer" style="font-size: 80%;">Know more about this module <a href="{{ help_url }}" target="_blank">here</a></div>
                </div>
            </div></div>'''
        else:
            html = '''<div class="col-lg-12"><div class="panel panel-danger">
                <div class="panel-heading">
                    <h3 class="panel-title">
                        {{- name -}}
                        <span class="pull-right glyphicon glyphicon-thumbs-down"></span>
                    </h3>
                </div>
                <div id="counter" class="panel-collapse">
                    <div class="panel-body">
                        <div class="col-lg-12">
                            <h4>Something wrong with collecting stats from database...</h4>
                        </div>
                    </div>
                    <div class="panel-footer" style="font-size: 80%;">Know more about this module <a href="{{ help_url }}" target="_blank">here</a></div>
                </div>
            </div></div>'''
            self.status = False

        t = Template(html)

        return t.render(name=self.name, data=self.result, help_url=self.get_help_url())

    def get_data(self, as_html=True):
        if as_html:
            return self.template()
        return self.result

    @property
    def name(self):
        return self.__addon__().replace('Addon', '')

    def execute(self, *args, **kwargs):
        self.result = page_view_stats.list(include_all=True)

    @staticmethod
    def __addon__():
        return 'ViewStatsAddon'
