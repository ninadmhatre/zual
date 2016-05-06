# -*- coding: utf-8 -*- 

__author__ = 'Ninad Mhatre'

from addonpy.IAddonInfo import IAddonInfo
from jinja2 import Template
from libs.AddonReturnType import AddonReturnType
import os


class SiteLogViewerAddon(IAddonInfo, AddonReturnType):
    result = None
    status = True

    def execute(self, *args, **kwargs):
        config = args[0]
        base = config.get('BASE_DIR')
        log_file = config['LOGGER']['FILE']['FILE']
        log_full_path = os.path.join(base, log_file)

        with open(log_full_path, 'r') as log_file:
            self.result = log_file.read().split('\n')
        
    def template(self):
        html = '''<div class="col-lg-12">
        <div class="panel panel-success">
           <div class="panel-heading">
              <h3 class="panel-title">
                {{- name -}}
                <span class="pull-right glyphicon glyphicon-thumbs-up"></span>
              </h3>
           </div>
           <div id="logviewer" class="panel-collapse">
                <div class="panel-body">
                    <pre class="prettyprint language-py" style="height: 500px;">
                        {%- for line in result -%}
{{ line }}<br>
                        {%- endfor -%}
                    </pre>
                </div>
           </div>
        </div></div>
        '''

        t = Template(html)
        return t.render(name=self.name, result=self.result, help_url=self.get_help_url())

    def get_data(self, as_html=True):
        if as_html:
            return self.template()
        return self.result

    @property
    def name(self):
        return 'Site Log'
 
    @staticmethod
    def __addon__():
        return 'SiteLogViewerAddon'
