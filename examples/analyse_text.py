from argparse import ArgumentParser

from text_analysis_helpers.text import TextAnalyser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("--output", default="analysis_result.html")
    parser.add_argument("filename")

    return parser.parse_args()


def main():
    args = get_arguments()

    analyser = TextAnalyser()
    analysis_result = analyser.analyse_file(args.filename)
    analysis_result.save(args.output)


if __name__ == "__main__":
    main()
