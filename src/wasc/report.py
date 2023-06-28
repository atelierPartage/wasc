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
    crit_list : list
        The list of criteria

    Methods
    -------
    bs_dict(self) :
        returns a dictionary containing URLs associated with their
        BeautifulSoup objects
    crit_list(self) :
        returns the list of criteria to analyze
    execute(self) :
        returns a dictionary containing the test results for each criterion and
        each URL
    """
    def __init__(self, label : str, url : str, criteria : list) :
        """
        It constructs all the necessary attributes for the report object

        Parameters
        ----------
        label : str
            The description of the website
        url : str
            The URL of the website
        crit_dict : dict
            The dictionary of criteria names associated to their checkers
            names to analyze

        Raises
        ------
        ValueError
            if the dictionary of URLs is empty
            if the dictionary of criteria is empty
        """
        if not label :
            msg = "No label given"
            raise ValueError(msg)
        if not url :
            msg = "No URL given"
            raise ValueError(msg)
        if not criteria :
            msg = "No criterion given in criteria list"
            raise ValueError(msg)
        self.__label = label
        self.__url = url
        self.__bs_obj = None
        self.__criteria = criteria

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
        This method returns dictionary containing the test results for each
        criterion and each URL. It goes through the criteria list and the
        BeautifulSoup object dictionary and analyzes each criterion for each URL

        Parameters
        ----------
        None

        Returns
        -------
        result : dict
            The dictionary containing the test results for each criterion and
            each URL
        """
        header = {
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36" ,
            "referer" : "https://www.google.com/"
            }
        response = requests.get(self.url, headers=header, timeout = 1)
        if response.status_code == requests.codes.ok :
            self.__bs_obj = bs4.BeautifulSoup(response.content, "html.parser")
        else:
            return {"bad response" : response.status_code}
        result = {}
        if self.__bs_obj:
            for crit in self.__criteria :
                result[crit.name] = crit.execute(self.__bs_obj, self.url)
        return result
