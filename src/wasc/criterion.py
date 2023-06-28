# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
Module criterion

Provides Criterion class that creates criterion objects composed
of checkers from the checker factory.

Class
-----
Criterion
"""
from wasc.checker_factory import checker_factory


class Criterion :
    """Criterion
    A class to represent a Criterion

    Attributes
    ----------
    name : str
        The name of the criterion
    checkers : list
        The list of checker object composing the criterion

    Methods
    -------
    name(self) :
        returns the name of the criterion
    checkers(self) :
        returns the list of object checker that compose the criterion
    execute(self, url) :
        returns a dictionary containing returns a dictionary with the name of
        the checkers associated with their result
    """
    def __init__(self, name : str, checkers : list) :
        """
        It constructs all the necessary attributes for the criterion object

        Parameters
        ----------
        name : str
            The name of the criterion
        checkers : list
            The list of the checker names composing the criterion

        Raises
        ------
        ValueError
            if the checkers list is empty
        """
        if checkers == [] :
            msg = "No checker given in checker list"
            raise ValueError(msg)
        self.__name = name
        self.__checkers = [checker_factory.create(checker) for checker in checkers]

    @property
    def name(self) :
        """
        This method returns the name of the criterion

        Parameters
        ----------
        None

        Returns
        -------
        self.__name : str
            The name of the criterion
        """
        return self.__name

    def execute(self, web_page, url) -> dict :
        """
        This method allows to analyze the bs4.BeautifulSoup object passed in
        parameter according to the current criterion

        Parameters
        ----------
        web_page : bs4.BeautifulSoup
            The BeautifulSoup object created from  url
        url : str
            The URL of the analyzed web page

        Returns
        -------
        bool : True if the beautifulsoup object has at least one head tag, if
        not it returns False
        """
        return {checker.description : checker.execute(web_page, url) for checker in self.__checkers}
