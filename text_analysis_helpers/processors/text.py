import itertools

from rake.rake import Rake
from rake.stoplists import get_stoplist_file_path
from textstat.textstat import textstat
import numpy as np

from nltk import sent_tokenize, word_tokenize

from text_analysis_helpers.models import TextStatistics


def extract_keywords(text, keyword_stop_list=None):
    keyword_stop_list = keyword_stop_list or "SmartStoplist.txt"
    rake = Rake(get_stoplist_file_path(keyword_stop_list))

    keywords = rake.run(text)

    keywords = {
        keyword: score
        for keyword, score in keywords
    }

    return keywords


def calculate_readability_scores(text):
    score_functions = [
        "flesch_reading_ease", "smog_index", "flesch_kincaid_grade",
        "coleman_liau_index", "automated_readability_index",
        "dale_chall_readability_score", "difficult_words",
        "linsear_write_formula", "gunning_fog", "text_standard"
    ]

    return {
        score_function: getattr(textstat, score_function)(text)
        for score_function in score_functions
    }


def calculate_text_statistics(text):
    sentences = sent_tokenize(text)
    sentence_words = [word_tokenize(sentence) for sentence in sentences]
    words = list(itertools.chain(*sentence_words))

    sentence_word_counts = np.array(
        [len(sentence) for sentence in sentence_words])

    return TextStatistics(
        sentence_count=len(sentences),
        word_count=len(words),
        mean_sentence_word_count=sentence_word_counts.mean(),
        median_sentence_word_count=np.median(sentence_word_counts),
        min_sentence_word_count=sentence_word_counts.min(),
        max_sentence_word_count=sentence_word_counts.max(),
        average_sentence_word_count=np.average(sentence_word_counts),
        sentence_word_count_std=sentence_word_counts.std(),
        sentence_word_count_variance=sentence_word_counts.var()
    )
