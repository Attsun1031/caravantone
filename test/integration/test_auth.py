# -*- coding: utf-8 -*-
import pyramid.testing as testing

from caravantone.testing import IntegrationTestBase
from caravantone.dao import UserRecord, db_session
from caravantone.view.user import add_artist


class TestLoginCheck(IntegrationTestBase):

    def setUp(self):
        super(TestLoginCheck, self).setUp()
        self.u = UserRecord(name='test_user')
        db_session.add(self.u)
        db_session.commit()

    def test_when_user_id_not_in_session_then_abort(self):
        # setup
        req = testing.DummyRequest(params=dict(name='Omer Klein', freebase_topic_id='/music/omer_klein'))

        # exercise & verify
        res = add_artist(None, req)
        self.assertEqual(res.status, '401 Unauthorized')

    def test_when_user_not_found_then_abort(self):
        # setup
        self.config.testing_securitypolicy(userid='99999:hoge')
        req = testing.DummyRequest(params=dict(name='Omer Klein', freebase_topic_id='/music/omer_klein'))

        # exercise & verify
        res = add_artist(None, req)
        self.assertEqual(res.status, '401 Unauthorized')


if __name__ == '__main__':
    import unittest
    unittest.main()
