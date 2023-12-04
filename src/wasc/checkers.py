# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1

import re

import bs4
from trafilatura import extract, fetch_url

from wasc.abstract_checker import AbstractChecker
from wasc.utils import FAIL, OK, PRESENT, check_and_correct_url

mentions = "non|partiellement|totalement"
ACCESS_PATTERN = re.compile("Accessibilité[ \xa0]:[ \xa0](" + mentions + ")[ \xa0]conforme", re.IGNORECASE)

class HeadNbChecker(AbstractChecker) :
    """HeadNbChecker
    A class to test the number of <head> tags in a page.
    """
    def __init__(self) :
        super().__init__("HeadNbChecker", "Nombre de <head>")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        return len(web_page.find_all(name="head"))

class HeadLvlChecker(AbstractChecker) :
    """HeadLvlChecker
    Get the depth of <head> tags in a web page.
    """
    def __init__(self) :
        super().__init__("HeadLvlChecker", "Profondeurs des <head>")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        head_tag = web_page.find_all("head")
        return [len(list(tag.parents)) - 1 for tag in head_tag] if head_tag else []

class AccessChecker(AbstractChecker) :
    """AccessChecker
    Check the presence of "Accessibilité" RGAA4 mention on the web page.
        1 - Search in <footer>
        2 - Search in <div id="footer">
        3 - Search in the whole page
    """
    def __init__(self) :
        super().__init__("AccessChecker", "Mention accessibilité")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        mention = ""
        footer = web_page.footer
        if footer:
            mention = footer.find_all(string = ACCESS_PATTERN)
        else:
            footer = web_page.find(id="footer")
            if footer:
                mention = footer.find_all(string = ACCESS_PATTERN)
            else:
                mention = web_page.find_all(string = ACCESS_PATTERN)
        return mention[0].split(":")[1].strip() if mention else FAIL

class AccessLinkChecker(AbstractChecker) :
    """AccessLinkChecker
    Check if a link ot an accessibility statement exists
    Search for a link as defined in search_link
        1 - in <footer>
        2 - in <div id="footer">
        3 - in the whole page
    """
    def __init__(self) :
        super().__init__("AccessLinkChecker", "Lien accessibilité")

    def search_link(self, web_page, root_url):
        # 1 - Try to find link in Mention Accessibilité
        access_tag = web_page.find("a", string=ACCESS_PATTERN)
        if access_tag :
            try:
                return check_and_correct_url(access_tag.attrs["href"], root_url)
            except Exception:
                return FAIL
        # 2 - Try to find text "accessibilité" in a link
        access_tag = web_page.find("a", string=re.compile("accessibilit", re.IGNORECASE))
        if access_tag :
            try:
                return check_and_correct_url(access_tag.attrs["href"], root_url)
            except Exception:
                return FAIL
        # 3 - Try to find a link that contains accessibilit in href
        link_tag = web_page.find("a", href=re.compile("accessibilit", re.IGNORECASE))
        if link_tag:
            try:
                return check_and_correct_url(link_tag.attrs["href"], root_url)
            except Exception:
                return FAIL
        return FAIL

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):
        footer = web_page.footer
        if footer:
            result = self.search_link(footer, root_url)
            if result != FAIL:
                return result
        footer = web_page.find(id="footer")
        if footer:
            result = self.search_link(footer, root_url)
            if result != FAIL:
                return result
        return self.search_link(web_page, root_url)

class AccessRateChecker(AbstractChecker) :
    """AccessRateChecker
    Returns the compliance rate (%) on the accessibility statement if found
    """
    def __init__(self) :
        super().__init__("AccessRateChecker", "Pourcentage de conformité")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):
        link_url = AccessLinkChecker().execute(web_page, root_url)
        if link_url == FAIL:
            return FAIL
        try:
            response = fetch_url(link_url)
            if response:
                result = extract(response, output_format="xml", include_links=True, no_fallback=True)
                link_page = bs4.BeautifulSoup(result, "html.parser")
                motif = re.compile(r"%", re.IGNORECASE)
                percent_tags = link_page.find_all(string = motif)
                for tag in percent_tags:
                    if "conformité" in tag:
                        m = re.search(r"\s(100|(\d{1,2}([\.\,]\d+)*)) *%", str(tag))
                        if m:
                            return str(float(str(m[1]).replace(",",".")))
        except Exception:
            return FAIL
        return FAIL

class LegalChecker(AbstractChecker) :
    """LegalChecker
    Test the presence of "Mentions légales" link on the web page.
    Try to find :
        * text "Mentions légales" (case insensitive) and check if a link exists
        * try the url root_url + "/mentions-legales" and check if a link exists
    Return the link to "Mentions légales" page if it exists, else fail
    """
    def __init__(self) :
        super().__init__("LegalChecker", "Mentions légales")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):
        motif = re.compile("Mentions* l[eé]gales*", re.IGNORECASE)
        legal_tags = web_page.find_all(string = motif)
        for tag in legal_tags:
            legal_tag = tag
            while legal_tag and legal_tag.name != "a" and legal_tag.name != "html":
                legal_tag = legal_tag.parent
            try :
                legal_link = check_and_correct_url(legal_tag.attrs["href"], root_url)
                return check_and_correct_url(legal_tag.attrs["href"], root_url)
            except KeyError :
                pass
        legal_link = check_and_correct_url("mentions-legales", root_url)
        try:
            response = fetch_url(legal_link, decode=False)
            if response and response.status == OK :
                return legal_link
        except Exception:
            return FAIL
        return FAIL

class LangChecker(AbstractChecker) :
    """LangChecker
    Check the presence of attribute lang in the html tag of the website
    """
    def __init__(self) :
        super().__init__("LangChecker", "Lang")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        try :
            if isinstance(web_page.html, bs4.Tag):
                return web_page.html.attrs["lang"]
        except KeyError :
            return FAIL

class DoctypeChecker(AbstractChecker) :
    """DoctypeChecker
    Check the presence of <!DOCTYPE html> at the beginning of HTML document (before <html>)
    """
    def __init__(self) :
        super().__init__("DoctypeChecker", "Doctype")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        current_pos = 0
        doctype_pos = 1
        html_pos = 0
        doctype_found = False
        for item in web_page.contents:
            if isinstance(item, bs4.Doctype):
                doctype_pos = current_pos
                doctype_found = True
                if item != "html":
                    return FAIL
            elif isinstance(item, bs4.Tag) and item.name == "html":
                html_pos = current_pos
            current_pos += 1
        if doctype_found and doctype_pos < html_pos:
            return "html"
        return FAIL

class HeaderChecker(AbstractChecker) :
    """HeaderChecker
    Check the presence of a unique <header> tag
    """
    def __init__(self) :
        super().__init__("HeaderChecker", "Header")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        return PRESENT if len(web_page.find_all(name="header")) == 1 else FAIL

class FooterChecker(AbstractChecker) :
    """FooterChecker
    Check the presence of a unique <footer> tag
    """
    def __init__(self) :
        super().__init__("FooterChecker", "Footer")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        return PRESENT if len(web_page.find_all(name="footer")) == 1 else FAIL

class ContactLinkChecker(AbstractChecker) :
    """ContactLinkChecker
    Check the presence of contact link in the page
    """
    def __init__(self) :
        super().__init__("ContactLinkChecker", "Lien Contact")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):
        link_tags = web_page.find_all(href=re.compile("(contact|ecrire)"))
        for tag in link_tags:
            try :
                return check_and_correct_url(tag.attrs["href"], root_url)
            except KeyError :
                pass
        return FAIL
