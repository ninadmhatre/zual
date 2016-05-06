__author__ = 'Ninad Mhatre'

from addonpy.IAddonInfo import IAddonInfo
from jinja2 import Template
from libs.AddonReturnType import AddonReturnType
import json


class RequestParamsAddon(IAddonInfo, AddonReturnType):
    result = {}
    status = True

    def execute(self, *args, **kwargs):
        r = args[1]
        for d in dir(r):
            if d.startswith('_') or d in ('cookies', 'headers'):
                continue

            val = getattr(r, d)
            if isinstance(val, dict):
                self.result[d] = {}
                for k, v in val.items():
                    self.result[d][k] = v
            else:
                self.result[d] = val

        import pprint
        # pprint.pprint(self.result, indent=1)

        self.result = pprint.pformat(self.result, indent=2)

    def template(self):
        html = '<h3>Failed to parse <code>request</code> object!</h3>'

        if self.result:
            html = '''<div class="col-lg-12"><div class="panel panel-success">
                <div class="panel-heading">
                    <h3 class="panel-title">
                        {{- name -}}
                        <span class="pull-right glyphicon glyphicon-thumbs-up"></span>
                    </h3>
                </div>
                <div id="requestparam" class="panel-collapse">
                    <div class="panel-body">
                        <div class="col-lg-12">
                            <pre class="prettyprint linenums language-js">
                                {{- data -}}
                            </pre>
                        </div>
                    </div>
                    <div class="panel-footer" style="font-size: 80%;">Know more about this module <a href="{{ help_url }}" target="_blank">here</a></div>
                </div>
            </div></div>'''

        t = Template(html)

        return t.render(name=self.name, data=self.result, help_url=self.get_help_url())

    def get_data(self, as_html=True):
        if as_html:
            return self.template()
        return self.result

    @property
    def name(self):
        return 'What is "request" made of?'

    @staticmethod
    def __addon__():
        return 'RequestParamsAddon'
