"""
Module checker

Provides an AbstractChecker class which defines how to create checkers.
A checker is meant to be the smallest possible test on website content.

Classes
-------
AbstractChecker(abc.ABC)

"""
import abc

from bs4 import BeautifulSoup


class AbstractChecker(abc.ABC) :
    """AbstractChecker
    Abstract Checker class declares the abstract method execute that
    needs to be implemented

    Attributes
    ----------
    description : str
        The description of the checker

    Methods
    -------
    execute(self, url) :
        Abstract method
    """
    def __init__(self, description : str) :
        """
        Sets the description of the checker

        Parameters
        ----------
        description : str
            The description of the checker
        """
        self.__description = description

    @property
    def description(self) :
        """
        Returns the description of the checker

        Parameters
        ----------
        None

        Returns
        -------
        description : str
            The description of the checker
        """
        return self.__description

    @abc.abstractmethod
    def execute(self, web_page: BeautifulSoup, url: str = "") -> dict:
        """
        Abstract method that needs to be implemented in subclasses

        Parameters
        ----------
        web_page : BeautifulSoup
            A BeautifulSoup object representing the web page

        Returns
        -------
         : dict
            A dictionary containing the results of the execution
        """
