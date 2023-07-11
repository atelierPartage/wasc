# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
import pytest

from wasc import utils


class TestReadCheckers:
    def test_no_file(self):
        with pytest.raises(FileNotFoundError):
            utils.read_checkers("foo.txt")
    def test_read_crit_example(self):
        expected_checkers = {
            "HeadNbChecker", "HeadLvlChecker",
            "AccessChecker", "AccessLinkChecker", "AccessRateChecker",
            "LegalChecker", "LangChecker", "DoctypeChecker"
        }
        read_checkers = utils.read_checkers("tests/data/checkers_example.csv")
        assert isinstance(read_checkers, list)
        assert set(read_checkers) == expected_checkers

class TestReadWebsites:
    def test_no_file(self):
        with pytest.raises(FileNotFoundError):
            utils.read_websites("foo.txt")
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
        assert not utils.check_and_correct_url("", "")

    def test_correct(self):
        assert utils.check_and_correct_url(EXAMPLE_TEST_URL, "https://www.example.com") == EXAMPLE_TEST_URL
        assert utils.check_and_correct_url("/fr/test/", EXAMPLE_ROOT_SLASH) == EXAMPLE_TEST_URL
        assert utils.check_and_correct_url("fr/test/", EXAMPLE_ROOT_SLASH) == EXAMPLE_TEST_URL
        assert utils.check_and_correct_url("/fr/test/", EXAMPLE_ROOT) == EXAMPLE_TEST_URL
