import sys

import requests

from text_analysis_helpers.html import HtmlAnalyser


def main():
    response = requests.get(sys.argv[1])

    analyser = HtmlAnalyser()
    result = analyser.analyse(response.text)

    print(result)


if __name__ == "__main__":
    main()
