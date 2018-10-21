from argparse import ArgumentParser

from text_analysis_helpers.html import HtmlAnalyser
from text_analysis_helpers.helpers import render_html_analysis_result


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("--output", default="analysis_result.html")
    parser.add_argument("url")

    return parser.parse_args()


def main():
    args = get_arguments()

    analyser = HtmlAnalyser()
    analysis_result = analyser.analyse_url(args.url)
    content = render_html_analysis_result(analysis_result)

    with open(args.output, "w") as f:
        f.write(content)
