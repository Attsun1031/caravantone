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
        from caravantone.dao import Base
        Base.metadata.create_all(checkfirst=False)
        self._setUp()

    def tearDown(self):
        from caravantone.dao import Base, db_session
        try:
            db_session.close()
        finally:
            Base.metadata.drop_all(checkfirst=False)

    def _setUp(self):
        pass

    def assert_record_equal(self, expected, actual):
        assert_record_equal(self, expected, actual)
