
import pytest
from bs4 import BeautifulSoup

import wasc.default_checkers as dft

BS_PARSER = "html.parser"

VALID_BASIC_HTML = """<!DOCTYPE html>
<html lang="fr">
    <head>
    </head>
    <body>
    </body>
    <footer>
    </footer>
</html>
"""

BAD_DOCTYPE = """<!DOCTYPE toto>
<html lang="fr">
    <head>
    </head>
    <body>
    </body>
    <footer>
    </footer>
</html>
"""

NO_DOCTYPE = """<html lang="fr">
    <head>
    </head>
    <body>
    </body>
    <footer>
    </footer>
</html>
"""

class TestDoctypeChecker:
    def test_doctype_checker_init(self):
        doctype_checker = dft.DoctypeChecker()
        assert doctype_checker.name == "DoctypeChecker"
        assert doctype_checker.description == "Doctype"

    def test_doctype_checker_valid(self):
        doctype_checker = dft.DoctypeChecker()
        basic_webpage = BeautifulSoup(VALID_BASIC_HTML, BS_PARSER)
        assert doctype_checker.execute(basic_webpage, "")

    def test_doctype_checker_bad_doctype(self):
        doctype_checker = dft.DoctypeChecker()
        basic_webpage = BeautifulSoup(BAD_DOCTYPE, BS_PARSER)
        assert not doctype_checker.execute(basic_webpage, "")

    def test_doctype_checker_no_doctype(self):
        doctype_checker = dft.DoctypeChecker()
        basic_webpage = BeautifulSoup(NO_DOCTYPE, BS_PARSER)
        assert not doctype_checker.execute(basic_webpage, "")
    