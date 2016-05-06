# -*- coding: utf-8 -*-

__author__ = 'Ninad Mhatre'


from addonpy.IAddonInfo import IAddonInfo
from libs.RedisCache import RedisCache
from libs.AddonReturnType import AddonReturnType
from jinja2 import Template


# Sample Output
# {'used_memory_lua': 36864, 'config_file': '', 'uptime_in_seconds': 267,
#  'repl_backlog_first_byte_offset': 0, 'blocked_clients': 0, 'aof_rewrite_in_progress': 0,
# 'used_memory_human': '796.83K', 'migrate_cached_sockets': 0, 'instantaneous_ops_per_sec': 0,
# 'aof_last_rewrite_time_sec': -1, 'lru_clock': 16144256, 'cluster_enabled': 0, 'redis_version': '3.0.5',
# 'redis_git_dirty': 0, 'used_memory_peak_human': '796.83K',
# 'cmdstat_ping': {'usec': 5, 'calls': 1, 'usec_per_call': 5.0},
# 'latest_fork_usec': 0, 'rdb_changes_since_last_save': 0, 'instantaneous_input_kbps': 0.0,
# 'aof_last_write_status': 'ok', 'connected_slaves': 0, 'aof_last_bgrewrite_status': 'ok',
# 'total_net_input_bytes': 37, 'master_repl_offset': 0, 'used_cpu_sys': 0.37,
# 'redis_mode': 'standalone', 'hz': 10, 'rdb_last_save_time': 1458984565,
# 'rdb_last_bgsave_status': 'ok', 'rdb_current_bgsave_time_sec': -1,
# 'client_biggest_input_buf': 0, 'keyspace_misses': 0, 'total_commands_processed': 1,
# 'aof_current_rewrite_time_sec': -1, 'repl_backlog_size': 1048576, 'used_memory': 815952,
# 'sync_partial_ok': 0, 'expired_keys': 0, 'used_cpu_user': 0.13, 'repl_backlog_histlen': 0,
# 'rejected_connections': 0, 'uptime_in_days': 0, 'aof_enabled': 0, 'os': 'Linux 4.2.0-34-generic x86_64',
# 'redis_git_sha1': 0, 'connected_clients': 1, 'used_cpu_sys_children': 0.0, 'arch_bits': 64,
# 'keyspace_hits': 0, 'total_connections_received': 1, 'total_net_output_bytes': 7,
# 'used_memory_rss': 4501504, 'pubsub_channels': 0, 'redis_build_id': '33b20773abdbdb2',
# 'sync_full': 0, 'repl_backlog_active': 0, 'used_cpu_user_children': 0.0,
# 'multiplexing_api': 'epoll', 'loading': 0, 'client_longest_output_list': 0,
# 'role': 'master', 'run_id': 'bf87695d7cfa5e4537c1da8ca7c2034ffe5a1deb',
# 'aof_rewrite_scheduled': 0, 'gcc_version': '5.2.1', 'mem_allocator': 'jemalloc-3.6.0',
# 'sync_partial_err': 0, 'rdb_last_bgsave_time_sec': -1, 'process_id': 11645,
# 'used_memory_peak': 815952, 'evicted_keys': 0, 'tcp_port': 6379, 'mem_fragmentation_ratio': 5.52,
# 'pubsub_patterns': 0, 'instantaneous_output_kbps': 0.0, 'rdb_bgsave_in_progress': 0}


class RedisAddon(IAddonInfo, AddonReturnType):
    result = None
    status = True  # Data received properly

    def execute(self, *args, **kwargs):
        r_instance = RedisCache()
        data = r_instance.info()

        self.result = {}

        if not data:
            return

        keys = ('redis_version', 'redis_mode', 'uptime_in_seconds', 'used_memory_human', 'used_memory_peak_human',
                'used_cpu_sys', 'expired_keys', 'uptime_in_days',
                'connected_clients', 'arch_bits', 'total_connections_received', 'role', 'evicted_keys',
                'tcp_port', 'mem_fragmentation_ratio')

        nested_keys = (('db0', 'keys', 'total_keys'),)

        for key in keys:
            self.result[key] = data[key]

        for k in nested_keys:
            self.result[k[2]] = data[k[0]][k[1]]

    def template(self):
        keys = ('redis_version', 'redis_mode', 'arch_bits', 'uptime_in_seconds',
                'used_memory_human', 'used_memory_peak_human',
                'used_cpu_sys', 'expired_keys', 'uptime_in_days',
                'connected_clients', 'total_connections_received', 'role', 'evicted_keys',
                'tcp_port', 'mem_fragmentation_ratio', 'total_keys')

        if self.result:
            html = '''<div class="col-lg-12"><div class="panel panel-success">
                <div class="panel-heading">
                    <h3 class="panel-title">
                        {{- name -}}
                        <span class="pull-right glyphicon glyphicon-thumbs-up"></span>
                    </h3>
                </div>
                <div id="redis" class="panel-collapse">
                    <div class="panel-body">
                        <div class="col-lg-8">
                            <table class="table table-bordered table-responsive">
                            {% for k in keys %}
                                <tr>
                                    <td>{{ k|replace('_', ' ') }}</td>
                                    <td>{{ data[k] }}</td>
                                </tr>
                            {% endfor %}
                            </table>
                        </div>
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
                <div id="redis" class="panel-collapse">
                    <div class="panel-body">
                        <div class="col-lg-12">
                            <h4>Redis seems to be down! please check...</h4>
                        </div>
                    </div>
                    <div class="panel-footer" style="font-size: 80%;">Know more about this module <a href="{{ help_url }}" target="_blank">here</a></div>
                </div>
            </div></div>
            '''
            self.status = False

        t = Template(html)

        return t.render(name=self.name, keys=keys, data=self.result, help_url=self.get_help_url())

    def get_data(self, as_html=True):
        if as_html:
            return self.template()
        return self.result

    @property
    def name(self):
        return self.__addon__().replace('Addon', ' Info')

    @staticmethod
    def __addon__():
        return 'RedisAddon'
