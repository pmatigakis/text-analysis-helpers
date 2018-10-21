from jinja2.loaders import PackageLoader
from jinja2 import Environment


def render_html_analysis_result(analysis_result,
                                template="html_analysis_result.html"):
    loader = PackageLoader('text_analysis_helpers', 'templates')
    env = Environment(loader=loader)
    template = env.get_template(template)

    return template.render(analysis_result=analysis_result)
