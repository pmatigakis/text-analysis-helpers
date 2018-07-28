from unittest import TestCase, main
from os import path, getcwd

from text_analysis_helpers.html import HtmlAnalyser


class HtmlAnalyserTests(TestCase):
    def test_analyse_content(self):
        page_file = path.join(getcwd(), "data", "page1.html")
        with open(page_file) as f:
            content = f.read()

        analyser = HtmlAnalyser()
        result = analyser.analyse(content)

        self.assertEqual(result.web_page_content.html, content)
        self.assertEqual(result.web_page_content.title, "test page 1")
        self.assertTrue(result.web_page_content.text.startswith(
            "Lorem ipsum dolor sit amet"))
        self.assertTrue(result.web_page_content.text.endswith(
            "lectus id ornare."))
        self.assertEqual(len(result.web_page_content.text), 1608)
        self.assertEqual(len(result.text_data.keywords), 66)
        self.assertAlmostEqual(
            max(result.text_data.keywords.values()), 62.366666, 3)
        self.assertAlmostEqual(
            min(result.text_data.keywords.values()), 1.0, 3)
        self.assertAlmostEqual(
            result.text_data.keywords["ut laoreet nisi ligula"],
            14.6818181, 3
        )
        self.assertDictEqual(
            result.social_network_data.twitter,
            {
                "card": "summary_large_image",
                "creator": "@example",
                "description": "test page 1 twitter description",
                "image:src": "https://example.com/image_2.png",
                "site": "@example_site"
            }
        )
        self.assertDictEqual(
            result.social_network_data.opengraph,
            {
                "_url": None,
                "description": "test page 1 description",
                "image": "https://example.com/image_1.png",
                "scrape": False,
                "site_name": "test page 1 site",
                "title": "test page 1 title",
                "type": "article",
                "url": "https://example.com"
            }
        )


if __name__ == "__main__":
    main()
