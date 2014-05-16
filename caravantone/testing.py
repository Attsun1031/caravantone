# -*- coding: utf-8 -*-

from unittest import TestCase


def setup4testing():
    """overwrite configurations for testing"""
    from caravantone.app import app
    app.config.from_object('caravantone.config.TestConfig')


def assert_record_equal(obj, expected, actual):
    """equality assertion function for sqlalchemy ORM object.

    :param expected: expected object
    :param actual: actual object
    """
    for column_name in actual.__table__.columns.keys():
        e_attr = getattr(expected, column_name)
        a_attr = getattr(actual, column_name)
        msg = '{column_name} is not equal. expected: {e_attr}, actual: {a_attr}'.format(**locals())
        obj.assertEqual(e_attr, a_attr, msg)


class TestCaseBase(TestCase):
    pass


class DBTestCaseBase(TestCaseBase):
    """base class for testing which touches database"""

    def setUp(self):
        from sqlalchemy.exc import OperationalError
        from caravantone.dao import Base
        try:
            Base.metadata.drop_all(checkfirst=False)
        except OperationalError:
            pass
        Base.metadata.create_all(checkfirst=False)
        self._setUp()

    def tearDown(self):
        from caravantone.dao import db_session
        db_session.close()

    def _setUp(self):
        pass


class AppTestBase(DBTestCaseBase):

    def setUp(self):
        from caravantone import app
        from caravantone.view import configure
        configure(app)
        app.config['TESTING'] = True
        self.app = app.test_client()
        super(AppTestBase, self).setUp()
