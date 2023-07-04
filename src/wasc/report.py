"""
Module report

This module provides the class Report that creates report objects composed
of criteria and BeautifulSoup objects representing URLs.

class
-----
Audit
"""

import bs4
import requests

from wasc.utils import HEADER


class Report :
    """
    A class to represent areport

    Attributes
    ----------
    label : str
        The description of the website
    url : str
        The URL of the website
    bs_obj : BeautifulSoup
        The BeautifulSoup object created
    checkers_list : list
        The list of checkers

    Methods
    -------
    bs_dict(self) :
        returns a dictionary containing URLs associated with their
        BeautifulSoup objects
    checkers_list(self) :
        returns the list of checkers
    execute(self) :
        returns a dictionary containing, for each URL, the test results for each checker
    """
    def __init__(self, label : str, url : str, checkers : list) :
        """
        It constructs all the necessary attributes for the report object

        Parameters
        ----------
        label : str
            The description of the website
        url : str
            The URL of the website
        checkers_list : list
            The list of checkers

        Raises
        ------
        ValueError
            if the dictionary of URLs is empty
            if the list of checkers is empty
        """
        self.__label = label
        self.__url = url
        self.__bs_obj = None
        self.__checkers = checkers
        self.__error = ""

    @property
    def url(self) :
        """
        This method returns the URL

        Parameters
        ----------
        None

        Returns
        -------
        self.__url : str
            The url
        """
        return self.__url

    @property
    def label(self) :
        """
        This method returns the label

        Parameters
        ----------
        None

        Returns
        -------
        self.__label : str
            The label
        """
        return self.__label

    def execute(self) :
        """
        This method returns a DataFrame containing test results where:
            * Each line correspond to an organisation (one URL)
            * Each column correspond to a checker

        Parameters
        ----------
        None

        Returns
        -------
        result : dict
            The dictionary containing the test results for each criterion and
            each URL
        """
        try:
            response = requests.get(self.url, headers=HEADER, timeout = 1)
            if response.status_code == requests.codes.ok :
                self.__bs_obj = bs4.BeautifulSoup(response.content, "html.parser")
            else:
                self.__error = "HTML Error Status " + str(response.status_code)
        except Exception as e:
            self.__error = str(e)
        starter = [self.__label, self.__url, self.__error]
        results = [checker.execute(self.__bs_obj, self.url) if self.__bs_obj else "" for checker in self.__checkers]
        return starter + results
