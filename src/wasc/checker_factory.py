# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
Module checker_factory

Provides a Factory design pattern for instantiation of AbstractCheckers.

For further usage of the factory, import checker_factory object from this module.
"""
import wasc.checkers as chk


class CheckerFactory :
    """CheckerFactory
    Factory design pattern to record and to create Checkers objects
    """
    def __init__(self) :
        """
        Sets the empty dictionary checker_dict.
        """
        self.__checker_dict = {}

    def register(self, checker_name : str, checker_class) :
        """
        Registers a new checker by specifying its name and
        the associated checker subclass of AbstractChecker
        """
        self.__checker_dict[checker_name] = checker_class

    def create(self, checker_name : str):
        """
        Returns a Checker object given its name (must be registered name)
        """
        return self.__checker_dict[checker_name]()

    def available(self):
        """
        Returns the list of checkers names without order
        """
        return list(self.__checker_dict.keys())

    def is_registered(self, checker_name : str):
        """
        Returns True if checker_name exists in the dictionary of checkers
        """
        return checker_name in self.__checker_dict

checker_factory = CheckerFactory()
checker_factory.register("AccessChecker", chk.AccessChecker)
checker_factory.register("AccessLinkChecker", chk.AccessLinkChecker)
checker_factory.register("AccessRateChecker", chk.AccessRateChecker)
checker_factory.register("ContactLinkChecker", chk.ContactLinkChecker)
checker_factory.register("DoctypeChecker", chk.DoctypeChecker)
checker_factory.register("FooterChecker", chk.FooterChecker)
checker_factory.register("HeaderChecker", chk.HeaderChecker)
checker_factory.register("HeadLvlChecker", chk.HeadLvlChecker)
checker_factory.register("HeadNbChecker", chk.HeadNbChecker)
checker_factory.register("LangChecker", chk.LangChecker)
checker_factory.register("LegalChecker", chk.LegalChecker)
