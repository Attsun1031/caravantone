# -*- coding: utf-8 -*-
from caravantone.model.base import Entity, Field
from caravantone.testing import TestCaseBase


children = [1, 2, 3]
class TestEntity(Entity):

    def __get_children(self):
        if self._children is None:
            self._children = children
        return self._children

    __fields__ = (Field('id', mandatory=True), Field('name'), Field('age', 20), Field('sex', 'male'),
                  Field('children', fget=__get_children))

    def get_old(self):
        self._age += 1


class TestEntityAttributes(TestCaseBase):
    def test_attr_set(self):
        e = TestEntity(id=1, name="hoge", sex="female")
        self.assertEqual(e.id, 1)
        self.assertEqual(e.name, "hoge")
        self.assertEqual(e.age, 20)
        self.assertEqual(e.sex, "female")

        e.get_old()
        self.assertEqual(e.age, 21)

    def test_mandatory_param_missed_then_raise_value_error(self):
        with self.assertRaises(ValueError):
            TestEntity(name="hoge", age=20, sex="male")

    def test_optional_param_missed_then_not_raise_value_error(self):
        e = TestEntity(id=1)
        self.assertEqual(e.id, 1)
        self.assertEqual(e.name, None)

    def test_equal(self):
        self.assertEqual(TestEntity(id=1, name="fuga", age=20), TestEntity(id=1, name="fuga", age=20))
        self.assertNotEqual(TestEntity(id=2, name="fuga", age=20), TestEntity(id=1, name="fuga", age=20))

    def test_specify_fget(self):
        self.assertEqual(TestEntity(id=1).children, children)
        self.assertEqual(TestEntity(id=1, children=[5, 6, 7]).children, [5, 6, 7])


if __name__ == '__main__':
    import unittest
    unittest.main()
