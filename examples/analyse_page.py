import sys
from pprint import PrettyPrinter

import requests

from text_analysis_helpers.html import HtmlAnalyser


def main():
    response = requests.get(sys.argv[1])

    analyser = HtmlAnalyser()
    result = analyser.process_content(response.text)

    pp = PrettyPrinter(indent=4)
    pp.pprint(result)


if __name__ == "__main__":
    main()
