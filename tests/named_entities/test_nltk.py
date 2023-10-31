from unittest import TestCase

from text_analysis_helpers.named_entities.nltk import NltkNamedEntityExtractor


class NltkNamedEntityExtractorTests(TestCase):
    def test_extract_named_entities(self):
        extractor = NltkNamedEntityExtractor()
        document = (
            "Carl Edward Sagan was an American astronomer and science "
            "communicator."
        )
        entities = extractor.extract_named_entities(document)

        self.assertDictEqual(
            entities, {"PERSON": {"Edward Sagan", "Carl"}, "GPE": {"American"}}
        )

    def test_extract_named_entities_with_empty_document(self):
        extractor = NltkNamedEntityExtractor()
        entities = extractor.extract_named_entities("")

        self.assertDictEqual(entities, {})
