from textstat.textstat import textstat


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
