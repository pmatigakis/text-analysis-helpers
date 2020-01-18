from argparse import ArgumentParser

from text_analysis_helpers.html import HtmlAnalyser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("--output", default="analysis_result.html")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("url")

    return parser.parse_args()


def main():
    args = get_arguments()

    analyser = HtmlAnalyser()
    analysis_result = analyser.analyse_url(args.url)

    if args.json:
        analysis_result.save_json(args.output)
    else:
        analysis_result.save(args.output)


if __name__ == "__main__":
    main()
