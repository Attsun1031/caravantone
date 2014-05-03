# -*- coding: utf-8 -*-

import caravantone.testing as testing
testing.setup4testing()

import caravantone.model.user as user
from caravantone.dao import db_session, OauthToken, User


class TestWhenSignUpWithExistingOauth(testing.DBTestCaseBase):

    def _setUp(self):
        self.user_name = 'user1'
        self.u = User(name='user1')
        self.o = OauthToken(provider_type=1, access_token='token', access_secret='secret', user=self.u)
        db_session.add_all([self.u, self.o])
        db_session.commit()

    def test_then_the_user_id_returned(self):
        # exercise SUT
        user_id = user.sign_up_with_oauth('token', 'secret', 1, 'user1')

        # verify
        self.assertEqual(user_id, self.u.id)

    def test_then_oauth_token_is_not_registered(self):
        # exercise SUT
        _ = user.sign_up_with_oauth('token', 'secret', 1, 'user1')

        # verify
        self.assertEqual(len(OauthToken.query.all()), 1)


class TestWhenSignUpWithNewOauth(testing.DBTestCaseBase):
    def test_then_new_user_id_returned(self):
        # exercise SUT
        user_id = user.sign_up_with_oauth('token', 'secret', 1, 'user1')

        # verify
        self.assertEqual(1, user_id)

    def test_then_new_user_registered(self):
        # exercise SUT
        _ = user.sign_up_with_oauth('token', 'secret', 1, 'user1')

        # verify
        u = User(id=1, name='user1')
        self.assert_record_equal(u, User.query.first())

    def test_then_new_oauth_token_registered(self):
        # exercise SUT
        _ = user.sign_up_with_oauth('token', 'secret', 1, 'user1')

        # verify
        o = OauthToken(access_token='token', access_secret='secret', user_id=1, provider_type=1)
        self.assert_record_equal(o, OauthToken.query.first())


class TestWhenCommitFailed(testing.DBTestCaseBase):
    def _setUp(self):
        from unittest import mock
        patcher = mock.patch('caravantone.model.user.db_session')
        self.addCleanup(patcher.stop)
        self.db_session = patcher.start()
        self.db_session.commit.side_effect = Exception

    def test_then_rollback_and_raise_exception(self):
        with self.assertRaises(Exception):
            user.sign_up_with_oauth('token', 'secret', 1, 'user1')
        self.assertIsNone(OauthToken.query.first())
        self.assertIsNone(User.query.first())


if __name__ == '__main__':
    import unittest
    unittest.main()