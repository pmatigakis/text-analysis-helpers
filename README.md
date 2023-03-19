# Introduction

Text-analysis-helpers is a collection of classes and functions for text analysis.

# Installation

A Python 3 interpreter is required. It is recommended to install the package in
a virtual environment in order to avoid corrupting the system's Python interpreter
packages.

Install the package using pip.

```bash
pip install text-analysis-helpers

python -m nltk.downloader "punkt"
python -m nltk.downloader "averaged_perceptron_tagger"
python -m nltk.downloader "maxent_ne_chunker"
python -m nltk.downloader "words"
python -m nltk.downloader "stopwords"
```

# Usage

You can use the HtmlAnalyser object to analyse the contents of a url.

```python
from text_analysis_helpers.html import HtmlAnalyser

analyser = HtmlAnalyser()
analysis_result = analyser.analyse_url("https://www.bbc.com/sport/formula1/64983451")

analysis_result.save("analysis_result.json")
```

You can see the scripts in the `examples` folder for some usage examples.

There is also an cli utility that can be used to analyse a url. For example to
analyse a url and save the analysis result to a json encoded file execute the
following command in the terminal.

```bash
text-analysis-helpers-cli analyse-url --output analysis_result.json https://www.bbc.com/sport/formula1/64983451
```
