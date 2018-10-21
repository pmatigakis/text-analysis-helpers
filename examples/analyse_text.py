from argparse import ArgumentParser

from text_analysis_helpers.text import TextAnalyser
from text_analysis_helpers.downloaders import download_web_page
from text_analysis_helpers.processors.html import extract_page_content


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("--output", default="analysis_result.html")
    parser.add_argument("url")

    return parser.parse_args()


def main():
    args = get_arguments()

    web_page = download_web_page(args.url)
    text = extract_page_content(web_page.html)

    analyser = TextAnalyser()
    analysis_result = analyser.analyse(text)
    analysis_result.save(args.output)


if __name__ == "__main__":
    main()
