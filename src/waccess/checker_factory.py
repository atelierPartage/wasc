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
import waccess.flb_checkers as flb


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

checker_factory = CheckerFactory()
checker_factory.register("FLBT01", flb.FLBT01)
checker_factory.register("FLBT02", flb.FLBT02)
checker_factory.register("FLBT03", flb.FLBT03)
checker_factory.register("FLBT04", flb.FLBT04)
checker_factory.register("FLBT05", flb.FLBT05)
checker_factory.register("FLBT06", flb.FLBT06)
checker_factory.register("FLBT07", flb.FLBT07)
