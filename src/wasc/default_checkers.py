# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
Module default_checker

Provides custom classes of checkers inherited from AbstractChecker.
Checkers are used to analyze the content of web pages as Beautiful soup objects.
Present Checkers were defined with the help of François le Berre.

Classes
-------
DFTT01(AbstractChecker) :
    Test the presence of tags <HEAD>
DFTT02(AbstractChecker) :
    Test the depth of tags <HEAD>
AccessChecker(AbstractChecker) :
    Test the presence of "Accessibilité" in the page
AccessLinkChecker(AbstractChecker) :
    Test if a link exist to the accessibility page
AccessRateChecker(AbstractChecker) :
    Test the presence of a compliance rate (%) on the accessibility statement
LegalChecker(AbstractChecker) :
    Test the presence of "mention légales" link on the web page
LangChecker(AbstractChecker) :
    Test the presence of the language in the header of the HTML page
DoctypeChecker(AbstractChecker) :
    Test the presence of Doctype in the web page
"""
import functools
import re

import bs4
import requests

from wasc.abstract_checker import AbstractChecker
from wasc.utils import HEADER, check_and_correct_url, find_link

FAIL = "échec"
mentions = "non|partiellement|totalement"
ACCESS_PATTERN = re.compile("Accessibilité[ \xa0]:[ \xa0](" + mentions + ")[ \xa0]conforme", re.IGNORECASE)

class DFTT01(AbstractChecker) :
    """DFTT01
    A class to test the presence of <head> tags.
    This class inherits from the AbstrastChecker.

    Attributes
    ----------
    name : str
        The name of the checker, i.e. a small identifier used in config files
    description : str
        The description of the checker, used in output

    Methods
    -------
    execute(self, web_page, url) -> dict :
        return the result of the checker
    """
    def __init__(self) :
        super().__init__("DFTT01", "Nombre de <head>")

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

class DFTT02(AbstractChecker) :
    """DFTT02
    A class to get the depth of <head> tags in a web page.
    This class inherits from the AbstrastChecker.

    Attributes
    ----------
    name : str
        The name of the checker

    Methods
    -------
    execute(self, web_page, url) :
        return the result of the checker
    """
    def __init__(self) :
        """
        It constructs all the necessary attributes for the DFTT02 class

        Parameters
        ----------
        None
        """
        super().__init__("DFTT02", "Profondeur des <head>")

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
    Check the presence of "Accessibilité" mention on the web page.

    Attributes
    ----------
    name : str
        The name of the checker
    description : str
        Description of the checker

    Methods
    -------
    execute(self, web_page, url) :
        return the level string or "non conforme"
    """
    def __init__(self) :
        """
        Sets the name and description of AccessChecker

        Parameters
        ----------
        None
        """
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
    Check that "Accessibilité" present on the web page is a link.

    Attributes
    ----------
    name : str
        The name of the checker
    description : str
        Description of the checker

    Methods
    -------
    execute(self, web_page, url) :
        return the link URL
    """
    def __init__(self) :
        """
        It constructs all the necessary attributes for the AccessLinkChecker class

        Parameters
        ----------
        None
        """
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
        # 3 - Check if there exists a link to a standard adresse root_url/accessibilite
        standard_link = check_and_correct_url("accessibilite", root_url)
        link_tags = web_page.find_all("a")
        for tag in link_tags:
            try :
                if check_and_correct_url(tag.attrs["href"], root_url) == standard_link:
                    return standard_link
            except KeyError :
                pass
        return FAIL

class AccessRateChecker(AbstractChecker) :
    """AccessRateChecker
    A class to represent the test of presence of compliance rate (%) on the accessibility statement
    web page. This class inherits from the AbstrastChecker class.

    Attributes
    ----------
    name : str
        The name of the checker
    description : str
        Description of the checker

    Methods
    -------
    execute(self, web_page, url) :
        return the result of the checker
    """
    def __init__(self) :
        """
        It constructs all the necessary attributes for the AccessRateChecker class

        Parameters
        ----------
        None
        """
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
        dict :
            The name of the checker is the key and the value is either False if there is no
            compliance rate (%), or the compliance rate (%)
        """
        checker_04 = AccessLinkChecker()
        access_url = checker_04.execute(web_page, root_url)
        if not access_url :
            return False
        response = requests.get(access_url, headers=HEADER, timeout = 1)
        if response.status_code == requests.codes.ok :
            access_page = bs4.BeautifulSoup(response.content, "html.parser")
        else :
            msg = f"The status_code is {response.status_code}, check the URL : {access_url}"
            raise ValueError(msg)
        for access_string in access_page.stripped_strings :
            match_string = re.search(r"Résultats des tests.*",access_string, \
                                     flags = re.IGNORECASE)
            if not match_string :
                continue
            if isinstance(access_page, bs4.NavigableString):
                access_tag = access_page.find(string = re.compile("Résultats des tests",\
                                                                   re.IGNORECASE)).parent
            iter_limit = 10
            while iter_limit and isinstance(access_tag, bs4.Tag) :
                for tag in access_tag.next_siblings :
                    if isinstance(tag, bs4.Tag) and tag.name :
                        statement = tag.find(string = re.compile("%"))
                        if statement :
                            statement_str = str(statement)
                            try:
                                index = statement_str.index("%")
                                counter = 0
                                for j in range(index-1, index-10, -1) :
                                    if statement_str[j] in "0123456789 ,." :
                                        counter += 1
                                    else :
                                        break
                                compliance_tmp = statement_str[index - counter:index + 1].split(" ")
                                compliance = functools.reduce(lambda x, y : x + y, compliance_tmp)
                                return compliance
                            except ValueError:
                                continue
                access_tag = access_tag.parent
                iter_limit -= 1
        return False

class LegalChecker(AbstractChecker) :
    """LegalChecker
    Test the presence of "Mentions légales" link on the web page.

    Attributes
    ----------
    name : str
        The name of the checker
    description : str
        Description of the checker

    Methods
    -------
    execute(self, web_page, url) :
        return the link to the page or fail
    """
    def __init__(self) :
        """
        It constructs all the necessary attributes for the LegalChecker class

        Parameters
        ----------
        None
        """
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
                return check_and_correct_url(legal_tag.attrs["href"], root_url)
            except KeyError :
                pass
        legal_link = check_and_correct_url("mentions-legales", root_url)
        response = requests.get(legal_link, headers=HEADER, timeout = 1)
        if response.status_code == requests.codes.ok :
            return legal_link
        return FAIL

class LangChecker(AbstractChecker) :
    """LangChecker
    Check the presence of attribute lang in the html tag of the website

    Attributes
    ----------
    name : str
        The name of the checker
    description : str
        Description of the checker

    Methods
    -------
    execute(self, web_page, url) :
        return the lang string or "non conforme"
    """
    def __init__(self) :
        """
        Sets the name and description of LangChecker

        Parameters
        ----------
        None
        """
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
    Check the presence of DOCTYPE at the beginning of HTML document
    (before <html>) + the type is html

    Attributes
    ----------
    name : str
        The name of the checker
    description : str
        Description of the checker

    Methods
    -------
    execute(self, web_page, url) :
        return "html" or "non conforme"
    """
    def __init__(self) :
        """
        Sets the name and description of DoctypeChecker

        Parameters
        ----------
        None
        """
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
        bool :
            True if Doctype is present, before <html> and has "html" value
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
