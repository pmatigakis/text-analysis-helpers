# Introduction

Text-analysis-helpers is a collection of classes and functions for text analysis.

## Installation

A Python 3 interpreter is required. It is recommended to install the package in
a virtual environment in order to avoid corrupting the system's Python interpeter
packages.

```bash
pip install text-analysis-helpers

python -m nltk.downloader "punkt"
python -m nltk.downloader "averaged_perceptron_tagger"
python -m nltk.downloader "maxent_ne_chunker"
python -m nltk.downloader "words"
```

## Usage

You can use the HtmlAnalyser object to analyse the contents of a url.

```python
from text_analysis_helpers.html import HtmlAnalyser

analyser = HtmlAnalyser()
analysis_result = analyser.analyse_url("http://www.add-a-url-here.com")

analysis_result.save("analysis_result.html")

```

You can see the scripts in the `examples` folder for some usage examples.

There is also an cli utility that can be used to analyse a url. For example to
analyse a url and save the analysis result to a json encoded file execute the
following command in the terminal.

```bash
text-analysis-helpers-cli analyse-url --json --output analysis_result.json https://www.the-url-to-analyse.com
```
