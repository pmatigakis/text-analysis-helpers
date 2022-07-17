from argparse import ArgumentParser

from text_analysis_helpers.html import HtmlAnalyser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("--output", default="analysis_result.json")
    parser.add_argument("url")

    return parser.parse_args()


def main():
    args = get_arguments()

    analyser = HtmlAnalyser()
    analysis_result = analyser.analyse_url(args.url)
    analysis_result.save(args.output)


if __name__ == "__main__":
    main()
