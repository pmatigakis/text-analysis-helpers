from gensim.summarization.summarizer import summarize
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from textstat.textstat import textstat

from text_analysis_helpers.keywords.rake import Rake


def extract_keywords(text):
    rake = Rake(
        word_tokenizer=word_tokenize,
        sentence_tokenizer=sent_tokenize,
        stop_words=stopwords.words("english"),
        delimiters=[",", "’", "‘", "“", "”", "“", "?", "—", "."],
    )

    return rake.extract_keywords(text)


def calculate_readability_scores(text):
    score_functions = [
        "flesch_reading_ease",
        "smog_index",
        "flesch_kincaid_grade",
        "coleman_liau_index",
        "automated_readability_index",
        "dale_chall_readability_score",
        "difficult_words",
        "linsear_write_formula",
        "gunning_fog",
        "text_standard",
    ]

    return {
        score_function: getattr(textstat, score_function)(text)
        for score_function in score_functions
    }


def create_summary(text):
    return summarize(text)
