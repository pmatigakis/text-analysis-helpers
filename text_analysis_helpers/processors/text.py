from rake.rake import Rake
from rake.stoplists import get_stoplist_file_path


def extract_keywords(text, keyword_stop_list=None):
    keyword_stop_list = keyword_stop_list or "SmartStoplist.txt"
    rake = Rake(get_stoplist_file_path(keyword_stop_list))

    keywords = rake.run(text)

    keywords = {
        keyword: score
        for keyword, score in keywords
    }

    return keywords
