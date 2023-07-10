# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1

import re

import bs4
from trafilatura import fetch_url

from wasc.abstract_checker import AbstractChecker
from wasc.utils import HEADER, check_and_correct_url, find_link

PRESENT = "présent"
FAIL = "échec"
OK = 200
mentions = "non|partiellement|totalement"
ACCESS_PATTERN = re.compile("Accessibilité[ \xa0]:[ \xa0](" + mentions + ")[ \xa0]conforme", re.IGNORECASE)

class HeadNbChecker(AbstractChecker) :
    """HeadNbChecker
    A class to test the number of <head> tags in a page.

    Attributes
    ----------
    name : str
        The name of the checker, i.e. a small identifier used in config files
    description : str
        The description of the checker, used in output

    Methods
    -------
    execute(self, web_page, url) -> dict :
        return the number of <head> tags (expected 1)
    """
    def __init__(self) :
        super().__init__("HeadNbChecker", "Nombre de <head>")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        """
        Gets the number of <head> tags in the web page

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        root_url : str
            The root URL of the analyzed web page (NOT USED HERE)

        Returns
        -------
         : int
            The number of <head> tags
        """
        return len(web_page.find_all(name="head"))

class HeadLvlChecker(AbstractChecker) :
    """HeadLvlChecker
    Get the depth of <head> tags in a web page.
    """
    def __init__(self) :
        super().__init__("HeadLvlChecker", "Profondeurs des <head>")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        """
        Returns the depth of <head> tags of the web page

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        root_url : str
            The root URL of the analyzed web page

        Returns
        -------
         : list
            The list of depth of head tags
        """
        head_tag = web_page.find_all("head")
        return [len(list(tag.parents)) - 1 for tag in head_tag] if head_tag else []

class AccessChecker(AbstractChecker) :
    """AccessChecker
    Check the presence of "Accessibilité" RGAA4 mention on the web page.
    """
    def __init__(self) :
        super().__init__("AccessChecker", "Mention accessibilité")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        """
        If there is a mention "Accessibilité", returns the level of accessibility,
        else "non conforme"

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        root_url : str
            The root URL of the analyzed web page

        Returns
        -------
        str :
            The level of accessibility or "non conforme"
        """
        mention = web_page.find_all(string = ACCESS_PATTERN)
        if mention :
            return mention[0].split(":")[1].strip()
        return FAIL

class AccessLinkChecker(AbstractChecker) :
    """AccessLinkChecker
    Check if a link ot an accessibility statement exists
    """
    def __init__(self) :
        super().__init__("AccessLinkChecker", "Lien accessibilité")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):
        """
        Search for a link to the accessibility page, either :
        * if the mention "Accessibilité" is a link
        * if there exists a link to root_url/accessibilite

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        root_url : str
            The root URL of the analyzed web page

        Returns
        -------
        dict :
            The name of the checker is the key and the value is either False if the mention
            "Accessibilité" / "Accessibility" is not a link, or it returns the URL of the link (str)
        """
        # 1- Check the link in the mention
        access_tag = web_page.find(string = ACCESS_PATTERN)
        if access_tag :
            link = find_link(access_tag, root_url)
            if link :
                return link
        # 2 - Find text "Déclaration d'accessibilité" and check if it's a link
        access_tag = web_page.find(string = "Déclaration d'accessibilité")
        if access_tag :
            link = find_link(access_tag, root_url)
            if link :
                return link
        # 3 - Check if there exists a link that ends with accessibilite or accessibility
        link_tags = web_page.find_all("a")
        for tag in link_tags:
            try :
                current_link = check_and_correct_url(tag.attrs["href"], root_url)
                if current_link.endswith("accessibility") or current_link.endswith("accessibilite"):
                    return current_link
            except KeyError :
                pass
        return FAIL

class AccessRateChecker(AbstractChecker) :
    """AccessRateChecker
    Get compliance rate (%) on the accessibility statement (if it exists)
    """
    def __init__(self) :
        super().__init__("AccessRateChecker", "Taux d'accessibilité")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):
        """
        This method performs the test on the beautifulsoup object passed in parameter and determines
        if there is a compliance rate (%) on the accessibility statement web page or not

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        root_url : str
            The root URL of the analyzed web page

        Returns
        -------
        str :
            the compliance rate (%), or "échec" if not found
        """
        link_url = AccessLinkChecker().execute(web_page, root_url)
        if link_url == FAIL:
            return FAIL
        try:
            response = fetch_url(link_url, decode=False)
            if response.status == OK :
                link_page = bs4.BeautifulSoup(response.data, "html.parser")
                motif = re.compile(r"%", re.IGNORECASE)
                percent_tags = link_page.find_all(string = motif)
                for tag in percent_tags:
                    if "conformité" in tag:
                        m = re.search(r"\s(100|(\d{1,2}([\.\,]\d+)*))\ *%", str(tag))
                        if m:
                            return str(m[1]) + "%"
        except Exception as e:
            return FAIL
        return FAIL

class LegalChecker(AbstractChecker) :
    """LegalChecker
    Test the presence of "Mentions légales" link on the web page.
    """
    def __init__(self) :
        super().__init__("LegalChecker", "Mentions légales")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):
        """
        Try to find :
        * text "Mentions légales" (case insensitive) and check if a link exists
        * try the url root_url + "/mentions-legales" and check if a link exists
        Return the link to "Mentions légales" page if it exists, else fail

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        root_url : str
            The root URL of the analyzed web page

        Returns
        -------
        str :
            The link to "Mentions légales" page if it exists, else fail
        """
        motif = re.compile("Mentions* l[eé]gales*", re.IGNORECASE)
        legal_tags = web_page.find_all(string = motif)
        for tag in legal_tags:
            legal_tag = tag
            while legal_tag and legal_tag.name != "a" and legal_tag.name != "html":
                legal_tag = legal_tag.parent
            try :
                legal_link = check_and_correct_url(legal_tag.attrs["href"], root_url)
                if root_url != legal_link:
                    return check_and_correct_url(legal_tag.attrs["href"], root_url)
            except KeyError :
                pass
        legal_link = check_and_correct_url("mentions-legales", root_url)
        try:
            response = fetch_url(legal_link, decode=False)
            if response.status == OK :
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
        """
        If the language is specified in the html tag, returns a string
        corresponding to the language of the web page, else "non conforme"

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created url
        root_url : str
            The root URL of the analyzed web page

        Returns
        -------
        str :
            the string of language or "non conforme"
        """
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
        """
        Check the presence of doctype in html document

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created url
        root_url : str
            The root URL of the analyzed web page

        Returns
        -------
        str :
            return "html" if valid else "échec"
        """
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
        """
        Check the presence of a unique <header> tag in web_page

        Returns
        -------
        str :
            return "present" if valid else "échec"
        """
        return PRESENT if len(web_page.find_all(name="header")) == 1 else FAIL

class FooterChecker(AbstractChecker) :
    """FooterChecker
    Check the presence of a unique <footer> tag
    """
    def __init__(self) :
        super().__init__("FooterChecker", "Footer")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):  # noqa: ARG002
        """
        Check the presence of a unique <footer> tag in web_page

        Returns
        -------
        str :
            return "present" if valid else "échec"
        """
        return PRESENT if len(web_page.find_all(name="footer")) == 1 else FAIL

class ContactLinkChecker(AbstractChecker) :
    """ContactLinkChecker
    Check the presence of a unique <footer> tag
    """
    def __init__(self) :
        super().__init__("ContactLinkChecker", "Lien Contact")

    def execute(self, web_page : bs4.BeautifulSoup, root_url : str):
        """
        Check the presence of a unique <footer> tag in web_page

        Returns
        -------
        str :
            return "present" if valid else "échec"
        """
        link_tags = web_page.find_all(href=re.compile("(contact|ecrire)"))
        for tag in link_tags:
            try :
                return check_and_correct_url(tag.attrs["href"], root_url)
            except KeyError :
                pass
        return FAIL
