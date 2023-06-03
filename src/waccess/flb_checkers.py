# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
Module flb_checker

Provides custom classes of checkers inherited from AbstractChecker.
Checkers are used to analyze the content of web pages as Beautiful soup objects.
Present Checkers were defined with the help of François le Berre (FLB).

Classes
-------
FLBT01(AbstractChecker) :
    Test the presence of tags <HEAD>
FLBT02(AbstractChecker) :
    Test the depth of tags <HEAD>
FLBT03(AbstractChecker) :
    Test the presence of the word "Accessibilité"
FLBT04(AbstractChecker) :
    Test if the word "Accessibilité" found in the page is a link (href)
FLBT05(AbstractChecker) :
    Test the presence of a compliance rate (%) on the accessibility statement
FLBT06(AbstractChecker) :
    Test the presence of "mention légales" link on the web page
FLBT07(AbstractChecker) :
    Test the presence of the language in the header of the HTML page
"""
import functools
import re

import bs4
import requests

from waccess.checker import AbstractChecker

ACC_STR    = "Accessibilité : "
ACC_SEC    = "Accessibilité\xa0: "
TOTAL_CONF = "totalement conforme"
PART_CONF  = "partiellement conforme"
NON_CONF   = "non conforme"

ACCESSIBILITY_PATTERN = re.compile("Accessibilité[ \xa0]: (.*) conforme", re.IGNORECASE)

class FLBT01(AbstractChecker) :
    """FLBT01
    A class to represent the test of presence of the head tag of a web page. This class inherits
    from the AbstrastChecker class.

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
        It constructs all the necessary attributes for the FLBT01 class

        Parameters
        ----------
        None
        """
        super().__init__("FLBT01")

    def execute(self, web_page : bs4.BeautifulSoup, url : str) -> dict :  # noqa: ARG002
        """
        This method performs the test on the beautifulsoup object passed in parameter and returns
        the number of head tags of the web page

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        url : str
            The URL of the analyzed web page

        Returns
        -------
        dict :
            The name of the checker is the key and the number of head tags is the value
        """
        return {self.name : len(web_page.find_all("head"))}

class FLBT02(AbstractChecker) :
    """FLBT02
    A class to represent the test of the depth of the head tag(s) of a web page. This class
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
        It constructs all the necessary attributes for the FLBT02 class

        Parameters
        ----------
        None
        """
        super().__init__("FLBT02")

    def execute(self, web_page : bs4.BeautifulSoup, url : str) -> dict :
        """
        This method performs the test on the beautifulsoup object passed in parameter and returns
        the depth of head tag(s) of the web page

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from url
        url : str
            The URL of the analyzed web page

        Returns
        -------
        dict :
            The name of the checker is the key and the value is the list of depth of head tags
        """
        checker_01 = FLBT01()
        head_tag = checker_01.execute(web_page, url)[checker_01.name]
        if not head_tag :
            return {self.name : False}
        result_dict = {self.name : []}
        for tag in web_page.find_all("head", limit = head_tag) :
            depth = len(list(tag.parents)) - 1
            result_dict[self.name].append(depth)
        return result_dict

class FLBT03(AbstractChecker) : #Mettre à jour docstrings
    """FLBT03
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
        It constructs all the necessary attributes for the FLBT03 class

        Parameters
        ----------
        None
        """
        super().__init__("FLBT03")

    def execute(self, web_page : bs4.BeautifulSoup, url : str) -> dict :  # noqa: ARG002
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
        mention =  web_page.find(string = ACCESSIBILITY_PATTERN)
        if mention :
            return {self.name : mention}
        return {self.name : False}

class FLBT04(AbstractChecker) :
    """FLBT04
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
        It constructs all the necessary attributes for the FLBT04 class

        Parameters
        ----------
        None
        """
        super().__init__("FLBT04")

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

    def execute(self, web_page : bs4.BeautifulSoup, url : str) -> dict :
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
        access_tag =  web_page.find(string = ACCESSIBILITY_PATTERN).parent
        if access_tag :
            while access_tag.name != "a" and access_tag.name != "html":
                access_tag = access_tag.parent
            try :
                tmp_url = access_tag.attrs["href"]
            except KeyError :
                return {self.name : False}
            return {self.name : self.get_access_url(tmp_url, url)}
        return {self.name : False}

class FLBT05(AbstractChecker) :
    """FLBT05
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
        It constructs all the necessary attributes for the FLBT05 class

        Parameters
        ----------
        None
        """
        super().__init__("FLBT05")

    def execute(self, web_page : bs4.BeautifulSoup, url : str) -> dict :
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
        checker_04 = FLBT04()
        access_url = checker_04.execute(web_page, url)[checker_04.name]
        if not access_url :
            return {self.name : False }
        response = requests.get(access_url, timeout = 1)
        if response.status_code == requests.codes.ok :
            access_page = bs4.BeautifulSoup(response.content, "html.parser")
        else :
            msg = f"The status_code is {response.status_code}, check the URL"
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
                                return {self.name : compliance}
                            except ValueError:
                                continue
                access_tag = access_tag.parent
                iter_limit -= 1
        return {self.name : False}


class FLBT06(AbstractChecker) : #Enlever footer
    """FLBT06
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
        It constructs all the necessary attributes for the FLBT06 class

        Parameters
        ----------
        None
        """
        super().__init__("FLBT06")

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

    def execute(self, web_page : bs4.BeautifulSoup, url : str) -> dict :
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
                        return {self.name : False}
                try :
                    tmp_url = legal_tag.attrs["href"]
                except KeyError :
                    return {self.name : False}
                return {self.name : self.get_legal_url(tmp_url, url)}
        return {self.name : False}


class FLBT07(AbstractChecker) :
    """FLBT07
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
        It constructs all the necessary attributes for the FLBT07 class

        Parameters
        ----------
        None
        """
        super().__init__("FLBT07")

    def execute(self, web_page : bs4.BeautifulSoup, url : str) -> dict :  # noqa: ARG002
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
            return {self.name : web_page.html.attrs["lang"]}
        except KeyError :
            return {self.name : False}
