# -*- coding: utf-8 -*-

from unittest import TestCase


def setup4testing():
    """overwrite configurations for testing"""
    from caravantone.app import app
    from caravantone.view import configure
    app.config.from_object('caravantone.config.TestConfig')
    configure(app)
    app.config['TESTING'] = True


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


class DBMixIn(object):

    def setUp(self):
        super(DBMixIn, self).setUp()
        from sqlalchemy.exc import OperationalError
        from caravantone.dao import Base
        try:
            Base.metadata.drop_all(checkfirst=False)
        except OperationalError:
            pass
        Base.metadata.create_all(checkfirst=False)

    def tearDown(self):
        from caravantone.dao import db_session
        db_session.close()


class DBTestCaseBase(DBMixIn, TestCaseBase):
    """base class for testing which touches database"""

    def setUp(self):
        super(DBTestCaseBase, self).setUp()
        # avoid to write `super.setUp` at each subclass.
        self._setUp()

    def _setUp(self):
        pass


class AppTestBase(DBMixIn, TestCaseBase):

    def setUp(self):
        super(AppTestBase, self).setUp()
        from caravantone.app import app
        self.app = app.test_client()
        # avoid to write `super.setUp` at each subclass.
        self._setUp()

    def _setUp(self):
        pass
