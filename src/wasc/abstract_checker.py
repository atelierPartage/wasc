# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
Module abstract_checker

Provides an AbstractChecker class which defines how to create checkers.
A checker is meant to be the smallest possible test on website content.
"""
import abc

from bs4 import BeautifulSoup


class AbstractChecker(abc.ABC) :
    """AbstractChecker
    Abstract Checker class declares the abstract method execute() that
    needs to be implemented in child classes
    """
    def __init__(self, name :str, description : str) :
        """
        Sets the name and description of checkers
        """
        self.__name = name
        self.__description = description

    @property
    def name(self) :
        """
        Returns the name of the checker
        """
        return self.__name

    @property
    def description(self) :
        """
        Returns the description of the checker
        """
        return self.__description

    @abc.abstractmethod
    def execute(self, bs_object: BeautifulSoup, url: str):
        """
        Abstract method that needs to be implemented in subclasses.
        Execute the tests of the checker
        """
