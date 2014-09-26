# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser
from unittest import TestCase

import pyramid.testing as testing

from caravantone.request import UserRetainRequetMixIn


config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'testing.ini'))
settings = dict(config['app:main'])


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


class DummyRequest(UserRetainRequetMixIn, testing.DummyRequest):
    pass


class TestCaseBase(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()


class DBMixIn(object):

    engine = None

    @classmethod
    def setUpClass(cls):
        from sqlalchemy import engine_from_config
        cls.engine = engine_from_config(settings, 'sqlalchemy.')

    def setUp(self):
        super(DBMixIn, self).setUp()

        from caravantone.dao import db_session, Base
        conn = self.engine.connect()
        self.trans = conn.begin()

        db_session.remove()

        # engineもconnectionもConnectableインターフェースを実装するオブジェクトなので代替可能な様子。
        # sqlalchemyのConnectionオブジェクトは、rawなコネクションを管理するオブジェクトでありコネクションそのものではない。
        db_session.configure(bind=conn)
        Base.metadata.bind = conn
        Base.query = db_session.query_property()

    def doCleanups(self):
        super(DBMixIn, self).doCleanups()
        from caravantone.dao import db_session
        self.trans.rollback()
        db_session.close()


class DBTestCaseBase(DBMixIn, TestCaseBase):
    """base class for testing which touches database"""


class IntegrationTestBase(DBTestCaseBase):
    """base class for integration testing"""


class FunctionalTestBase(DBTestCaseBase):
    """base class for functional testing"""
    @classmethod
    def setUpClass(cls):
        from caravantone import main
        from caravantone.dao import db_session
        cls.app = main({}, **settings)
        cls.engine = db_session.bind

    def setUp(self):
        from webtest import TestApp
        self.app = TestApp(self.app)
        super(FunctionalTestBase, self).setUp()
