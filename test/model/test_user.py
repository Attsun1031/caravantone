# -*- coding: utf-8 -*-

import caravantone.testing as testing
testing.setup4testing()

import caravantone.model.user as user
from caravantone.model.base import ValidationError
from caravantone.model.artist import Artist
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
        user_id = user.sign_up_with_oauth('token', 'secret', 1, 'user1').id

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
        user_id = user.sign_up_with_oauth('token', 'secret', 1, 'user1').id

        # verify
        self.assertEqual(1, user_id)

    def test_then_new_user_registered(self):
        # exercise SUT
        model = user.sign_up_with_oauth('token', 'secret', 1, 'user1')

        # verify
        u = UserRecord.query.get(1)
        self.assertEqual(u.name, model.name)

    def test_then_new_oauth_token_registered(self):
        # exercise SUT
        u = user.sign_up_with_oauth('token', 'secret', 1, 'user1')

        # verify
        model = u.oauth_tokens[0]
        record = OauthTokenRecord.query.first()
        self.assertEqual(model.access_token, record.access_token)
        self.assertEqual(model.access_secret, record.access_secret)
        self.assertEqual(model.provider.type_num, record.provider_type)


class TestAddArtists(testing.DBTestCaseBase):

    def test_when_add_one_then_the_artist_related_to_user(self):
        # setup
        self.user = UserRecord(name='test_user')
        self.artist = ArtistRecord(name='test_artist')
        db_session.add_all([self.artist, self.user])
        db_session.commit()

        # exercise SUT
        user_model = user_repository.find_by_id(self.user.id)
        artist_model = artist_repository.find_by_id(self.artist.id)
        user_model.check_artists(artist_model)
        user_repository.save(user_model)

        # verify
        user_model = user_repository.find_by_id(self.user.id)
        self.assertEqual(1, len(user_model.checked_artists))
        self.assertEqual(artist_model, user_model.checked_artists[0])

    def test_when_add_multi_then_artists_related_to_user(self):
        # setup
        self.user = UserRecord(name='test_user')
        self.artist1 = ArtistRecord(name='test_artist1')
        self.artist2 = ArtistRecord(name='test_artist2')
        db_session.add_all([self.artist1, self.artist2, self.user])
        db_session.commit()

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

    def test_illegal_type(self):
        a = Artist(name='the band')
        u = user.User(name='user', checked_artists=[a])
        self.assertEqual(u.checked_artists, [a])

        with self.assertRaises(ValidationError):
            user.User(name='user', checked_artists=[1])



class TestLoadArtist(testing.DBTestCaseBase):
    def test_lazy_load(self):
        # setup
        user = UserRecord(name='test_user')
        artist = ArtistRecord(name='test_artist')
        user.checked_artists.append(artist)
        db_session.add(user)
        db_session.commit()

        # exercise SUT
        user_model = user_repository.find_by_id(user.id)
        artist_model = artist_repository.find_by_id(artist.id)

        # not loaded before access
        self.assertIsNone(user_model._checked_artists)
        # loaded if touching accessor
        self.assertEqual(user_model.checked_artists, [artist_model])


if __name__ == '__main__':
    import unittest
    unittest.main()
