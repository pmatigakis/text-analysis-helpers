from logging import getLogger

from articles.mss.extractors import MSSArticleExtractor

logger = getLogger(__name__)


def extract_page_content(html_content):
    article_extractor = MSSArticleExtractor()

    return article_extractor.extract_article(html_content)


def extract_page_data(soup):
    title = soup.find("title")

    return {"title": title.text if title else None}


def extract_twitter_card(soup):
    card = {}

    for meta in soup.find_all("meta"):
        name = meta.get("name", "")
        if name.startswith("twitter:"):
            items = name.split(":")
            if len(items) < 2:
                msg = "Invalid twitter card value: twitter_card(%s)"
                logger.warning(msg, name)
                continue
            card[":".join(items[1:])] = meta.get("content")

    # if twitter card data could not be extracted then return None instead
    # of an empty dictionary
    if len(card) == 0:
        logger.warning("failed to extract twitter card")
        card = None

    return card
