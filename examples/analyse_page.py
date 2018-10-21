from argparse import ArgumentParser
from os import getcwd

from jinja2.loaders import FileSystemLoader
from jinja2 import Environment

from text_analysis_helpers.html import HtmlAnalyser
from text_analysis_helpers.downloaders import download_web_page


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("--output", default="analysis_result.html")
    parser.add_argument("url")

    return parser.parse_args()


def main():
    args = get_arguments()

    web_page = download_web_page(args.url)
    analyser = HtmlAnalyser()
    analysis_result = analyser.analyse(web_page)

    env = Environment(loader=FileSystemLoader(getcwd()))
    template = env.get_template("analysis_result_template.html")
    content = template.render(analysis_result=analysis_result)

    with open(args.output, "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
