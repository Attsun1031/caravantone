# -*- coding: utf-8 -*-
from wtforms import Form, Field, IntegerField, validators

from caravantone.model.base import Entity, ValidationError
from caravantone.model.form import AggregateField
from caravantone.testing import TestCaseBase


children = [1, 2, 3]
class TestForm(Form):
    id = IntegerField('id', [validators.DataRequired()])
    name = Field()
    age = IntegerField(default=20)
    sex = Field(default='male')
    children = AggregateField(IntegerField())


class TestEntity(Entity):

    _form_class = TestForm

    def _get_children(self):
        if self._children is None:
            self._children = children[:]
        return self._children

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
        with self.assertRaises(ValidationError):
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

    def test_specify_fset(self):
        e = TestEntity(id=1, children=[1, 2])
        new_values = [7, 8]
        e.children = new_values
        self.assertEqual(e.children, new_values)

        e.children = []
        self.assertEqual(e.children, [])


if __name__ == '__main__':
    import unittest
    unittest.main()
