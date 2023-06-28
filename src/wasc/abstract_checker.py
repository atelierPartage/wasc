# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
Module abstract_checker

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
    Abstract Checker class declares the abstract method execute() that
    needs to be implemented in child classes

    Attributes
    ----------
    name : str
        The name of the checker, i.e. a small identifier used in config files
    description : str
        The description of the checker, used in output

    Methods
    -------
    execute(self, bs_object, url) : dict
        Abstract method
    """
    def __init__(self, name :str, description : str) :
        """
        Sets the description of the checker

        Parameters
        ----------
        description : str
            The description of the checker
        """
        self.__name = name
        self.__description = description

    @property
    def name(self) :
        """
        Returns the name of the checker, i.e.
        a small identifier used in config files

        Parameters
        ----------
        None

        Returns
        -------
        name : str
            The name of the checker
        """
        return self.__name

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
    def execute(self, bs_object: BeautifulSoup, url: str) -> dict:
        """
        Abstract method that needs to be implemented in subclasses

        Parameters
        ----------
        bs_object : BeautifulSoup
            A BeautifulSoup object representing the web page
        url: str
            The url of the web page
        Returns
        -------
         : dict
            The data representing the result of the checker as a dictionary
        """
