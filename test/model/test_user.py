# -*- coding: utf-8 -*-

import caravantone.testing as testing
testing.setup4testing()

import caravantone.model.user as user
from caravantone.repository import user_repository, artist_repository
from caravantone.dao import db_session, OauthTokenRecord, UserRecord, ArtistRecord


class TestWhenSignUpWithExistingOauth(testing.DBTestCaseBase):

    def _setUp(self):
        self.user_name = 'user1'
        self.u = UserRecord(name='user1')
        self.o = OauthTokenRecord(provider_type=1, access_token='token', access_secret='secret', user=self.u)
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
        self.assertEqual(len(OauthTokenRecord.query.all()), 1)


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
        u = UserRecord(id=1, name='user1')
        self.assert_record_equal(u, UserRecord.query.first())

    def test_then_new_oauth_token_registered(self):
        # exercise SUT
        _ = user.sign_up_with_oauth('token', 'secret', 1, 'user1')

        # verify
        o = OauthTokenRecord(access_token='token', access_secret='secret', user_id=1, provider_type=1)
        self.assert_record_equal(o, OauthTokenRecord.query.first())


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
        self.assertIsNone(OauthTokenRecord.query.first())
        self.assertIsNone(UserRecord.query.first())


class TestAddToStreamWhenSingle(testing.DBTestCaseBase):
    def _setUp(self):
        self.user = UserRecord(name='test_user')
        self.artist = ArtistRecord(name='test_artist')
        db_session.add_all([self.artist, self.user])
        db_session.commit()

    def test_then_the_artist_related_to_user(self):
        # exercise SUT
        user_model = user_repository.find_by_id(self.user.id)
        artist_model = artist_repository.find_by_id(self.artist.id)
        user_model.check_artists(artist_model)
        user_repository.save(user_model)

        # verify
        user_model = user_repository.find_by_id(self.user.id)
        self.assertEqual(1, len(user_model.checked_artists))
        self.assertEqual(artist_model, user_model.checked_artists[0])


class TestAddToStreamWhenMulti(testing.DBTestCaseBase):
    def _setUp(self):
        self.user = UserRecord(name='test_user')
        self.artist1 = ArtistRecord(name='test_artist1')
        self.artist2 = ArtistRecord(name='test_artist2')
        db_session.add_all([self.artist1, self.artist2, self.user])
        db_session.commit()

    def test_then_artists_related_to_user(self):
        # exercise SUT
        user_model = user_repository.find_by_id(self.user.id)
        artist_model1 = artist_repository.find_by_id(self.artist1.id)
        artist_model2 = artist_repository.find_by_id(self.artist2.id)
        user_model.check_artists([artist_model1, artist_model2])

        user_repository.save(user_model, flush=True)

        # verify
        user_model = user_repository.find_by_id(self.user.id)
        self.assertEqual(2, len(user_model.checked_artists))
        self.assertEqual(artist_model1, user_model.checked_artists[0])
        self.assertEqual(artist_model2, user_model.checked_artists[1])


if __name__ == '__main__':
    import unittest
    unittest.main()
