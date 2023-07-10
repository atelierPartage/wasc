# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
Module checker_factory

Provides a Factory design pattern for instantiation of AbstractCheckers.

For further usage of the factory, import checker_factory object from this module.

Classes
-------
CheckerFactory

Objects
-------
checker_factory
"""
import wasc.checkers as chk


class CheckerFactory :
    """CheckerFactory
    Implements a Factory design pattern to record and to create Checkers objects

    Attributes
    ----------
    checker_dict : dict
        The dictionary of the different checkers (flag, subclass of AbstractChecker)

    Methods
    -------
    register(self, checker_name: str, checker_class) :
        Registers new checkers
    create(self, checker: str) :
        Returns a checker object
    """
    def __init__(self) :
        """
        Constructs the empty dictionary checker_dict.

        Parameters
        ----------
        None
        """
        self.__checker_dict = {}

    def register(self, checker_name : str, checker_class) :
        """
        Registers a new checker by specifying its name and
        the associated checker subclass of AbstractChecker

        Parameters
        ----------
        checker_name : str
            The checker name as used in config file
        checker_class : AbstractChecker subclass
            The checker subclass
        Returns
        -------
        None
        """
        self.__checker_dict[checker_name] = checker_class

    def create(self, checker_name : str):
        """
        Returns a Checker object given its name (must be registered name)

        Parameters
        ----------
        checker_name : str
            The checker name

        Returns
        -------
        The checker object corresponding to the checker name
        """
        return self.__checker_dict[checker_name]()

    def available(self):
        """
        Returns the list of checkers names

        Parameters
        ----------

        Returns
        -------
        : list
        The list of checkers names
        """
        return list(self.__checker_dict.keys())

    def is_registered(self, checker_name : str):
        """
        Returns the list of checkers as pair (checker.name, checker.description)

        Parameters
        ----------
        checker_name : str
            A checker name
        Returns
        -------
        : bool
        True is the checker name is known
        """
        return checker_name in self.__checker_dict

checker_factory = CheckerFactory()
checker_factory.register("HeadNbChecker", chk.HeadNbChecker)
checker_factory.register("HeadLvlChecker", chk.HeadLvlChecker)
checker_factory.register("AccessRateChecker", chk.AccessRateChecker)
checker_factory.register("LangChecker", chk.LangChecker)
checker_factory.register("DoctypeChecker", chk.DoctypeChecker)
checker_factory.register("AccessChecker", chk.AccessChecker)
checker_factory.register("AccessLinkChecker", chk.AccessLinkChecker)
checker_factory.register("LegalChecker", chk.LegalChecker)
checker_factory.register("HeaderChecker", chk.HeaderChecker)
checker_factory.register("FooterChecker", chk.FooterChecker)
checker_factory.register("ContactLinkChecker", chk.ContactLinkChecker)
