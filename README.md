# Introduction

Text-analysis-helpers is a collection of classes and functions for text analysis.

## Installation

Clone the repository and install it. It is recomended to install the package in
a virtual environment in order to avoid corrupting the system's Python interpeter
packages.

```bash
git clone git+https://github.com/pmatigakis/text-analysis-helpers.git
pip install -r requirements.txt .
python -m nltk.downloader "punkt"

```

## Usage

You can use the HtmlAnalyser object to analyse the contents of a url.

```python
from text_analysis_helpers.html import HtmlAnalyser

analyser = HtmlAnalyser()
analysis_result = analyser.analyse_url("http://www.add-a-domain-here.com")

analysis_result.save("analysis_result.html")

```
