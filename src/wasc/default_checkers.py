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
DFTT03(AbstractChecker) :
    Test the presence of the word "Accessibilité"
DFTT04(AbstractChecker) :
    Test if the word "Accessibilité" found in the page is a link (href)
DFTT05(AbstractChecker) :
    Test the presence of a compliance rate (%) on the accessibility statement
DFTT06(AbstractChecker) :
    Test the presence of "mention légales" link on the web page
DFTT07(AbstractChecker) :
    Test the presence of the language in the header of the HTML page
"""
import functools
import re

import bs4
import requests

from wasc.abstract_checker import AbstractChecker

HEADER = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    "referer" : "https://www.google.com/"
    }

ACCESSIBILITY_PATTERN = re.compile("Accessibilité[ \xa0]:[ \xa0](non|partiellement|totalement)[ \xa0]conforme", re.IGNORECASE)

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
        """
        It constructs all the necessary attributes for the DFTT01 class

        Parameters
        ----------
        None
        """
        super().__init__("DFTT01", "Nombre de <head>")

    def execute(self, web_page : bs4.BeautifulSoup, url : str):  # noqa: ARG002
        """
        Gets the number of <head> tags in the web page

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        url : str
            The URL of the analyzed web page (NOT USED HERE)

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

    def execute(self, web_page : bs4.BeautifulSoup, url : str):  # noqa: ARG002
        """
        Returns the depth of <head> tags of the web page

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        url : str
            The URL of the analyzed web page

        Returns
        -------
         : list
            The list of depth of head tags
        """
        head_tag = web_page.find_all("head")
        return [len(list(tag.parents)) - 1 for tag in head_tag] if head_tag else []

class DFTT03(AbstractChecker) : #Mettre à jour docstrings
    """DFTT03
    A class to represent the test of presence of the mention "Accessibilité" or "Accessibility" on
    the web page. This class inherits from the AbstrastChecker class.

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
        It constructs all the necessary attributes for the DFTT03 class

        Parameters
        ----------
        None
        """
        super().__init__("DFTT03", "Accessibilité")

    def execute(self, web_page : bs4.BeautifulSoup, url : str):  # noqa: ARG002
        """
        This method performs the test on the beautifulsoup object passed in parameter and determines
        if there is no mention "Accessibilité" or "Accessibility", or the level of
        accessibility if there is the mention

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        url : str
            The URL of the analyzed web page

        Returns
        -------
        dict :
            The name of the checker is the key and the value is either False if there is no mention
            "Accessibilité" or "Accessibility", or an int (1 if there is only the mention
            "Accessibilité" or "Accessibility", 2, 3, 4 if there is the level of accessibility,
            "Totalement", "Partiellement", "non", ect
        """
        mention = web_page.find_all(string = ACCESSIBILITY_PATTERN)
        # if isinstance(mention, str) :
        return mention if mention else False

class DFTT04(AbstractChecker) :
    """DFTT04
    A class to test if the mention of "Accessibilité" present on the web page is a link. This class
    inherits from the AbstrastChecker class.

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
        It constructs all the necessary attributes for the DFTT04 class

        Parameters
        ----------
        None
        """
        super().__init__("DFTT04", "Lien accessibilité")

    def get_access_url(self, tmp_url : str, url : str) -> str :
        """
        This method allows to retrieve the URL of the accessibility statement.
        home_url : the url of the home page

        Parameters
        ----------
        tmp_url : str
            The URL of the mention "Accessibilité" / "Accessibility" link
        url : str
            The URL of the analyzed web page

        Returns
        -------
        access_url : str
            The URL of the accessibility statement
        """
        if tmp_url.startswith("http") :
            return tmp_url
        if url.endswith("/fr") and tmp_url.startswith("/fr") :
            return url + tmp_url[3:]
        return url + tmp_url

    def execute(self, web_page : bs4.BeautifulSoup, url : str):
        """
        This method performs the test on the beautifulsoup object passed in parameter and determines
        if the mention "Accessibilité" / "Accessibility" is a link or not

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        url : str
            The URL of the analyzed web page

        Returns
        -------
        dict :
            The name of the checker is the key and the value is either False if the mention
            "Accessibilité" / "Accessibility" is not a link, or it returns the URL of the link (str)
        """
        access_tag = web_page.find(string = ACCESSIBILITY_PATTERN)
        if access_tag :
            while access_tag and access_tag.name != "a" and access_tag.name != "html":
                access_tag = access_tag.parent
            try :
                tmp_url = access_tag.attrs["href"]
            except KeyError :
                return False
            return self.get_access_url(tmp_url, url)
        return False

class DFTT05(AbstractChecker) :
    """DFTT05
    A class to represent the test of presence of compliance rate (%) on the accessibility statement
    web page. This class inherits from the AbstrastChecker class.

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
        It constructs all the necessary attributes for the DFTT05 class

        Parameters
        ----------
        None
        """
        super().__init__("DFTT05", "Taux d'accessibilité")

    def execute(self, web_page : bs4.BeautifulSoup, url : str):
        """
        This method performs the test on the beautifulsoup object passed in parameter and determines
        if there is a compliance rate (%) on the accessibility statement web page or not

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        url : str
            The URL of the analyzed web page

        Returns
        -------
        dict :
            The name of the checker is the key and the value is either False if there is no
            compliance rate (%), or the compliance rate (%)
        """
        checker_04 = DFTT04()
        access_url = checker_04.execute(web_page, url)
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
            access_tag = access_page.find(string = re.compile("Résultats des tests",\
                                                                   re.IGNORECASE)).parent
            iter_limit = 10
            while iter_limit :
                for tag in access_tag.next_siblings :
                    if tag.name :
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


class DFTT06(AbstractChecker) : #Enlever footer
    """DFTT06
    A class to represent the test of presence of "Mentions légales" link on the web page. This class
    inherits from the AbstrastChecker class.

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
        It constructs all the necessary attributes for the DFTT06 class

        Parameters
        ----------
        None
        """
        super().__init__("DFTT06", "Mentions légales")

    def get_legal_url(self, tmp_url : str, url : str) -> str :
        """
        This method allows to retrieve the complete URL of the "Mentions légales" link.
        home_url : the url of the home page

        Parameters
        ----------
        tmp_url : str
            The URL of "Mention légales" link
        url : str
            The URL of the analyzed web page

        Returns
        -------
        legal_url : str
            The complete URL of the "Mentions légales" link
        """
        if tmp_url.startswith("http") :
            legal_url = tmp_url
        elif url.endswith("/fr") and tmp_url.startswith("/fr") :
            legal_url = url + tmp_url[3:]
        else :
            home_url = url.split("/")
            home_url = home_url[0] + "//" + home_url[2]
            legal_url =  home_url + tmp_url
        return legal_url

    def execute(self, web_page : bs4.BeautifulSoup, url : str):
        """
        This method performs the test on the beautifulsoup object passed in parameter and determines
        if there is a "Mentions légales" link on the web page, and if yes, it retrieves the complete
        URL of the "Mentions légales" link

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        url : str
            The URL of the analyzed web page

        Returns
        -------
        dict :
            The name of the checker is the key and the value is either False if there is no
            "Mentions légales" link, or it returns the URL of the link (str)
        """
        if web_page.footer :
            for footer_string in web_page.footer.stripped_strings :
                match_string = re.search(r"légales.*",\
                                          footer_string, flags = re.IGNORECASE)
                if not match_string :
                    continue
                legal_tag = web_page.footer.find(string = re.compile("légales",\
                                                                       re.IGNORECASE)).parent
                while legal_tag.name != "a" :
                    legal_tag = legal_tag.parent
                    if legal_tag.name == "html" :
                        return False
                try :
                    tmp_url = legal_tag.attrs["href"]
                except KeyError :
                    return False
                return self.get_legal_url(tmp_url, url)
        return False


class DFTT07(AbstractChecker) :
    """DFTT07
    A class to represent the test of presence of the language in the header of the HTML page. This
    class inherits from the AbstrastChecker class.

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
        It constructs all the necessary attributes for the DFTT07 class

        Parameters
        ----------
        None
        """
        super().__init__("DFTT07", "Langage")

    def execute(self, web_page : bs4.BeautifulSoup, url : str):  # noqa: ARG002
        """
        This method performs the test on the beautifulsoup object passed in parameter and determines
        if the language is specified in the header of the HTML page. If yes, it returns a string
        corresponding to the language of the web page

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created url
        url : str
            The URL of the analyzed web page

        Returns
        -------
        dict :
            The name of the checker is the key and the value is either False if there is no language
            specified in the header of the HTML page, or it returns the language (str)
        """
        try :
            return web_page.html.attrs["lang"]
        except KeyError :
            return False
