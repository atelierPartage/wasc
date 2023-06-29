import pytest

from wasc import utils


class TestReadCriteria:
    def test_no_file(self):
        with pytest.raises(FileNotFoundError):
            utils.read_criteria_config("foo.txt")
    def test_not_yaml(self):
        utils.read_criteria_config("tests/data/url_example.csv")
    def test_read_crit_example(self):
        expected_criteria = {
            "Balise head" : ["DFTT01", "DFTT02"],
            "Mention Accessibilité" : ["DFTT03", "DFTT04", "DFTT05"],
            "Mention légale" : ["DFTT06"],
            "Langage" : ["DFTT07"]
        }
        crit_example = utils.read_criteria_config("tests/data/crit_example.yml")
        assert isinstance(crit_example, dict)
        for key, value in crit_example.items():
            assert key in expected_criteria.keys()
            assert value in expected_criteria.values()

class TestReadWebsites:
    def test_no_file(self):
        with pytest.raises(FileNotFoundError):
            utils.read_criteria_config("foo.txt")
    def test_read_url_example(self):
        expected_url = [
            ("Design Gouv", "https://design.numerique.gouv.fr/"),
            ("Example", "http://example.com")
        ]
        url_example = utils.read_websites("tests/data/url_example.csv")
        assert isinstance(url_example, list)
        for website in url_example:
            assert website in expected_url

EXAMPLE_TEST_URL = "https://www.example.com/fr/test"
EXAMPLE_ROOT = "https://www.example.com/fr"
EXAMPLE_ROOT_SLASH = "https://www.example.com/fr/"

class TestCheckAndCorrectUrl:
    def test_empty(self):
        assert utils.check_and_correct_url("", "") == "/"

    def test_correct(self):
        assert utils.check_and_correct_url(EXAMPLE_TEST_URL, "https://www.example.com") == EXAMPLE_TEST_URL

    def test_overlap(self):
        assert utils.check_and_correct_url("/fr/test", EXAMPLE_ROOT_SLASH) == EXAMPLE_TEST_URL
        assert utils.check_and_correct_url("fr/test", EXAMPLE_ROOT_SLASH) == EXAMPLE_TEST_URL
        assert utils.check_and_correct_url("/fr/test", EXAMPLE_ROOT) == EXAMPLE_TEST_URL

    def test_compose(self):
        assert utils.check_and_correct_url("test", EXAMPLE_ROOT_SLASH) == EXAMPLE_TEST_URL
        assert utils.check_and_correct_url("/test", EXAMPLE_ROOT_SLASH) == EXAMPLE_TEST_URL
        assert utils.check_and_correct_url("/test/", EXAMPLE_ROOT_SLASH) == EXAMPLE_TEST_URL
        assert utils.check_and_correct_url("/test/", EXAMPLE_ROOT) == EXAMPLE_TEST_URL
