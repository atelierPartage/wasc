# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
import wasc.checker_factory as fact


class TmpChecker:
    pass

class TestCheckerFactory:
    def test_checker_factory_init(self):
        tmp_factory = fact.CheckerFactory()
        assert isinstance(tmp_factory, fact.CheckerFactory)
    def test_checker_factory_register(self):
        tmp_factory = fact.CheckerFactory()
        tmp_factory.register("tmp_name", TmpChecker)
        assert tmp_factory.is_registered("tmp_name")
    def test_checker_factory_create(self):
        tmp_factory = fact.CheckerFactory()
        tmp_factory.register("tmp_name", TmpChecker)
        tmp_obj = tmp_factory.create("tmp_name")
        assert isinstance(tmp_obj, TmpChecker)
    def test_checker_factory_available(self):
        tmp_factory = fact.CheckerFactory()
        tmp_factory.register("tmp_name", TmpChecker)
        check_list = tmp_factory.available()
        assert check_list == ["tmp_name"]
