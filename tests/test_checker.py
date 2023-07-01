
from bs4 import BeautifulSoup

import wasc.default_checkers as dft

BS_PARSER = "html.parser"
FAIL = "échec"

class TestDoctypeChecker:
    def test_doctype_checker_init(self):
        doctype_checker = dft.DoctypeChecker()
        assert doctype_checker.name == "DoctypeChecker"
        assert doctype_checker.description == "Doctype"

    def test_doctype_checker_valid(self):
        test_html = "<!DOCTYPE html><html></html>"
        doctype_checker = dft.DoctypeChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert doctype_checker.execute(basic_webpage, "") == "html"

    def test_doctype_checker_bad_doctype(self):
        test_html = "<!DOCTYPE notvalid><html></html>"
        doctype_checker = dft.DoctypeChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert doctype_checker.execute(basic_webpage, "") == FAIL

    def test_doctype_checker_no_doctype(self):
        test_html = "<html></html>"
        doctype_checker = dft.DoctypeChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert doctype_checker.execute(basic_webpage, "") == FAIL

class TestLangChecker:
    def test_lang_checker_init(self):
        lang_checker = dft.LangChecker()
        assert lang_checker.name == "LangChecker"
        assert lang_checker.description == "Lang"

    def test_lang_checker_valid(self):
        test_html = '<!DOCTYPE html><html lang="fr"></html>'
        lang_checker = dft.LangChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert lang_checker.execute(basic_webpage, "") == "fr"

    def test_lang_checker_empty(self):
        test_html = "<!DOCTYPE html><html></html>"
        lang_checker = dft.LangChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert lang_checker.execute(basic_webpage, "") == FAIL

class TestAccessChecker:
    def test_access_checker_init(self):
        access_checker = dft.AccessChecker()
        assert access_checker.name == "AccessChecker"
        assert access_checker.description == "Accessibilité"

    def test_access_checker_fail1(self):
        test_html = "<!DOCTYPE html><html><body><div></div></body></html>"
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == FAIL

    def test_access_checker_fail2(self):
        test_html = "<!DOCTYPE html><html><body><div>Accessibilité : conforme partiellement</div></body></html>"
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == FAIL

    def test_access_checker_valid_non(self):
        test_html = "<!DOCTYPE html><html><body><div>Accessibilité : non conforme</div></body></html>"
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == "non conforme"

    def test_access_checker_valid_partiel(self):
        test_html = "<!DOCTYPE html><html><body><div>Accessibilité : partiellement conforme</div></body></html>"
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == "partiellement conforme"

    def test_access_checker_valid_total(self):
        test_html = "<!DOCTYPE html><html><body><div>Accessibilité : totalement conforme</div></body></html>"
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == "totalement conforme"

class TestAccessLinkChecker:
    def test_access_link_checker_init(self):
        access_link_checker = dft.AccessLinkChecker()
        assert access_link_checker.name == "AccessLinkChecker"
        assert access_link_checker.description == "Lien accessibilité"

    def test_access_checker_valid_mention(self):
        test_link = '<a href="/misc/accessibilite/">Accessibilité : totalement conforme</a>'
        test_html = "<!DOCTYPE html><html><body><div>" + test_link + "</div></body></html>"
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_link_checker.execute(basic_webpage, "https://www.example.com") == "https://www.example.com/misc/accessibilite"

    def test_access_checker_fail_mention(self):
        test_html = "<!DOCTYPE html><html><body><div>Accessibilité : totalement conforme</div></body></html>"
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_link_checker.execute(basic_webpage, "https://www.example.com") == FAIL

    def test_access_checker_valid_other(self):
        test_link = '<a href="/accessibilite/">Accessibilité</a>'
        test_html = "<!DOCTYPE html><html><body><footer>" + test_link + "</footer></body></html>"
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_link_checker.execute(basic_webpage, "https://www.example.com") == "https://www.example.com/accessibilite"

    def test_access_checker_fail_other(self):
        test_link = '<a href="/misc/accessibilite/">Accessibilité</a>'
        test_html = "<!DOCTYPE html><html><body><footer>" + test_link + "</footer></body></html>"
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_link_checker.execute(basic_webpage, "https://www.example.com") == FAIL
    
    def test_access_checker_fail_href(self):
        test_link = "<a>Accessibilité</a>"
        test_html = "<!DOCTYPE html><html><body><footer>" + test_link + "</footer></body></html>"
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_link_checker.execute(basic_webpage, "https://www.example.com") == FAIL
