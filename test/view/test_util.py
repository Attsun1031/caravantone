# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest
from wtforms import Form, validators, TextField

import caravantone.testing as testing
testing.setup4testing()

from caravantone import app
from caravantone.view.util import validate


class FormForTest(Form):
    name = TextField('name', [validators.InputRequired()])


@validate(FormForTest)
def view(form):
    return True


class TestValidateGetRequest(testing.TestCaseBase):

    def test_required_param_supplied(self):
        with app.test_request_context('/?name=hoge'):
            self.assertTrue(view())

    def test_require_param_not_supplied(self):
        with app.test_request_context('/?age=20'):
            with self.assertRaises(BadRequest):
                view()


class TestValidatePostRequest(testing.TestCaseBase):

    def test_required_param_supplied(self):
        with app.test_request_context(method='POST', data={'name': 'hoge'}):
            self.assertTrue(view())

    def test_require_param_not_supplied(self):
        with app.test_request_context(method='POST', data={'age': 20}):
            with self.assertRaises(BadRequest):
                view()


if __name__ == '__main__':
    import unittest
    unittest.main()
