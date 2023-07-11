# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
from bs4 import BeautifulSoup

import wasc.checkers as dft
from wasc.utils import FAIL, PRESENT

BS_PARSER = "html.parser"

DEFAULT_HTML_HEAD = "<!DOCTYPE html><html><head></head><body><div>"
DEFAULT_HTML_TAIL = "</div></body></html>"
DEFAULT_HTML_ROOT = "https://www.example.com"
DESIGN_NUM = "https://design.numerique.gouv.fr"
HTML_BODY_ONLY = "<!DOCTYPE html><html><body></body></html>"

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
        assert access_checker.description == "Mention accessibilité"

    def test_access_checker_fail1(self):
        test_html = DEFAULT_HTML_HEAD + DEFAULT_HTML_TAIL
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == FAIL

    def test_access_checker_fail2(self):
        test_html = DEFAULT_HTML_HEAD + "Accessibilité : conforme partiellement" + DEFAULT_HTML_TAIL
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == FAIL

    def test_access_checker_valid_non(self):
        test_html = DEFAULT_HTML_HEAD + "Accessibilité : non conforme" + DEFAULT_HTML_TAIL
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == "non conforme"

    def test_access_checker_valid_partiel(self):
        test_html = DEFAULT_HTML_HEAD + "Accessibilité : partiellement conforme" + DEFAULT_HTML_TAIL
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == "partiellement conforme"

    def test_access_checker_valid_total(self):
        test_html = DEFAULT_HTML_HEAD + "Accessibilité : totalement conforme" + DEFAULT_HTML_TAIL
        access_checker = dft.AccessChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_checker.execute(basic_webpage, "") == "totalement conforme"

class TestAccessLinkChecker:
    def test_access_link_checker_init(self):
        access_link_checker = dft.AccessLinkChecker()
        assert access_link_checker.name == "AccessLinkChecker"
        assert access_link_checker.description == "Lien accessibilité"

    def test_access_link_checker_valid_mention(self):
        test_link = '<a href="/accessibilite/">Accessibilité : non conforme</a>'
        test_html = DEFAULT_HTML_HEAD + test_link + DEFAULT_HTML_TAIL
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = DEFAULT_HTML_ROOT + "/accessibilite"
        assert access_link_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer

    def test_access_link_checker_fail_mention(self):
        test_html = DEFAULT_HTML_HEAD + "Accessibilité : totalement conforme" + DEFAULT_HTML_TAIL
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_link_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == FAIL

    def test_access_link_checker_valid_other(self):
        test_html = DEFAULT_HTML_HEAD + '<a href="/accessibilite/">Accessibilité</a>' + DEFAULT_HTML_TAIL
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_link_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == DEFAULT_HTML_ROOT + "/accessibilite"

    def test_access_link_checker_fail_other(self):
        test_html = DEFAULT_HTML_HEAD + '<a href="/misc/accessibilite/">Accessibilité</a>' + DEFAULT_HTML_TAIL
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = DEFAULT_HTML_ROOT + "/misc/accessibilite"
        assert access_link_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer

    def test_access_link_checker_fail_href(self):
        test_html = DEFAULT_HTML_HEAD + "<a>Accessibilité</a>" + DEFAULT_HTML_TAIL
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_link_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == FAIL

    def test_access_link_checker_decla(self):
        test_link = '<a href="/misc/accessibilite/">Déclaration d\'accessibilité</a>'
        test_html = DEFAULT_HTML_HEAD + test_link + DEFAULT_HTML_TAIL
        access_link_checker = dft.AccessLinkChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = DEFAULT_HTML_ROOT + "/misc/accessibilite"
        assert access_link_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer

class TestAccessRateChecker:
    def test_access_rate_checker_init(self):
        access_rate_checker = dft.AccessRateChecker()
        assert access_rate_checker.name == "AccessRateChecker"
        assert access_rate_checker.description == "Taux d'accessibilité"

    def test_access_rate_checker_valid(self):
        """
        Be Careful, this test use a real url that may change over time
        """
        test_link = '<a href="/misc/accessibilite/">Accessibilité : totalement conforme</a>'
        test_html = DEFAULT_HTML_HEAD + test_link + DEFAULT_HTML_TAIL
        access_rate_checker = dft.AccessRateChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_rate_checker.execute(basic_webpage, DESIGN_NUM) == "100%"

    def test_access_rate_checker_fail_link(self):
        test_html = DEFAULT_HTML_HEAD + "Accessibilité : non conforme" + DEFAULT_HTML_TAIL
        access_rate_checker = dft.AccessRateChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_rate_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == FAIL

    def test_access_rate_checker_fail_link2(self):
        test_link = '<a href="/misc/accessibilite/">Accessibilité : totalement conforme</a>'
        test_html = DEFAULT_HTML_HEAD + test_link + DEFAULT_HTML_TAIL
        access_rate_checker = dft.AccessRateChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert access_rate_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == FAIL

class TestLegalChecker:
    def test_mention_legales_checker_init(self):
        mention_legales_checker = dft.LegalChecker()
        assert mention_legales_checker.name == "LegalChecker"
        assert mention_legales_checker.description == "Mentions légales"

    def test_mention_legales_valid_mention1(self):
        test_html = DEFAULT_HTML_HEAD + '<a href="/misc/mentions-legales/">Mentions légales</a>' + DEFAULT_HTML_TAIL
        mention_legales_checker = dft.LegalChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = DEFAULT_HTML_ROOT + "/misc/mentions-legales"
        assert mention_legales_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer

    def test_mention_legales_valid_mention2(self):
        test_html = DEFAULT_HTML_HEAD + '<a href="/misc/mentions-legales/">mention legale</a>' + DEFAULT_HTML_TAIL
        mention_legales_checker = dft.LegalChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = DEFAULT_HTML_ROOT + "/misc/mentions-legales"
        assert mention_legales_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer

    def test_mention_legales_fail_mention(self):
        test_html = DEFAULT_HTML_HEAD + "Mentions légales" + DEFAULT_HTML_TAIL
        mention_legales_checker = dft.LegalChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert mention_legales_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == FAIL

    def test_mention_legales_valid_dftlink(self):
        test_html = DEFAULT_HTML_HEAD + "foo" + DEFAULT_HTML_TAIL
        mention_legales_checker = dft.LegalChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = "https://www.gouvernement.fr/mentions-legales"
        assert mention_legales_checker.execute(basic_webpage, "https://www.gouvernement.fr/") == answer

class TestHeadNbChecker:
    def test_head_nb_checker_init(self):
        head_nb_checker = dft.HeadNbChecker()
        assert head_nb_checker.name == "HeadNbChecker"
        assert head_nb_checker.description == "Nombre de <head>"
    def test_head_nb_valid_01(self):
        test_html = DEFAULT_HTML_HEAD + DEFAULT_HTML_TAIL
        head_nb_checker = dft.HeadNbChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = 1
        assert head_nb_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer
    def test_head_nb_valid_02(self):
        test_html = DEFAULT_HTML_HEAD + "<head></head>" + DEFAULT_HTML_TAIL
        head_nb_checker = dft.HeadNbChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = 2
        assert head_nb_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer
    def test_head_nb_fail(self):
        test_html = HTML_BODY_ONLY
        head_nb_checker = dft.HeadNbChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = 0
        assert head_nb_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer

class TestHeadLvlChecker:
    def test_head_lvl_checker_init(self):
        head_lvl_checker = dft.HeadLvlChecker()
        assert head_lvl_checker.name == "HeadLvlChecker"
        assert head_lvl_checker.description == "Profondeurs des <head>"
    def test_head_lvl_valid_01(self):
        test_html = DEFAULT_HTML_HEAD + DEFAULT_HTML_TAIL
        head_lvl_checker = dft.HeadLvlChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = [1]
        assert head_lvl_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer
    def test_head_lvl_valid_02(self):
        test_html = DEFAULT_HTML_HEAD + "<head></head>" + DEFAULT_HTML_TAIL
        head_lvl_checker = dft.HeadLvlChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = [1,3]
        assert head_lvl_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer
    def test_head_lvl_fail(self):
        test_html = HTML_BODY_ONLY
        head_lvl_checker = dft.HeadLvlChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        answer = []
        assert head_lvl_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == answer

class TestHeaderChecker:
    def test_header_checker_init(self):
        header_checker = dft.HeaderChecker()
        assert header_checker.name == "HeaderChecker"
        assert header_checker.description == "Header"

    def test_header_checker_fail(self):
        test_html = HTML_BODY_ONLY
        header_checker = dft.HeaderChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert header_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == FAIL

    def test_header_checker_present(self):
        test_html = "<!DOCTYPE html><html><body><header></header></body></html>"
        header_checker = dft.HeaderChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert header_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == PRESENT

class TestFooterChecker:
    def test_footer_checker_init(self):
        footer_checker = dft.FooterChecker()
        assert footer_checker.name == "FooterChecker"
        assert footer_checker.description == "Footer"

    def test_footer_checker_fail(self):
        test_html = HTML_BODY_ONLY
        footer_checker = dft.FooterChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert footer_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == FAIL

    def test_footer_checker_present(self):
        test_html = "<!DOCTYPE html><html><body><footer></footer></body></html>"
        footer_checker = dft.FooterChecker()
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        assert footer_checker.execute(basic_webpage, DEFAULT_HTML_ROOT) == PRESENT

class TestContactLinkChecker:
    def test_contact_link_checker_init(self):
        contact_link_checker = dft.ContactLinkChecker()
        assert contact_link_checker.name == "ContactLinkChecker"
        assert contact_link_checker.description == "Lien Contact"

    def test_contact_link_checker_valid(self):
        test_link = '<a href="/contact">Nous contacter</a>'
        test_html = DEFAULT_HTML_HEAD + test_link + DEFAULT_HTML_TAIL
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        contact_link_checker = dft.ContactLinkChecker()
        answer = "https://design.numerique.gouv.fr/contact"
        assert contact_link_checker.execute(basic_webpage, DESIGN_NUM) == answer

    def test_contact_link_checker_no_href(self):
        test_link = "<a>Nous contacter</a>"
        test_html = DEFAULT_HTML_HEAD + test_link + DEFAULT_HTML_TAIL
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        contact_link_checker = dft.ContactLinkChecker()
        assert contact_link_checker.execute(basic_webpage, DESIGN_NUM) == FAIL

    def test_contact_link_checker_bad_link(self):
        test_link = '<a href="/foo">Nous contacter</a>'
        test_html = DEFAULT_HTML_HEAD + test_link + DEFAULT_HTML_TAIL
        basic_webpage = BeautifulSoup(test_html, BS_PARSER)
        contact_link_checker = dft.ContactLinkChecker()
        assert contact_link_checker.execute(basic_webpage, DESIGN_NUM) == FAIL
