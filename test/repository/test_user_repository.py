# -*- coding: utf-8 -*-
from caravantone.testing import TestCaseBase, DBTestCaseBase, assert_record_equal
import caravantone.repository.user as user
from caravantone.repository import user_repository
from caravantone.repository.artist import ArtistMapper
from caravantone.model.user import User
from caravantone.dao import UserRecord, OauthTokenRecord, ArtistRecord


class TestUserMapper(TestCaseBase):

    def setUp(self):
        super(TestUserMapper, self).setUp()
        self.mapper = user.UserMapper(ArtistMapper(), user.OauthTokenMapper())

    def test_without_relation_then_no_relation_loaded(self):
        d = UserRecord(name='user')
        res = self.mapper.data2model(d)
        self.assertIsNone(res._checked_artists)
        self.assertIsNone(res._oauth_tokens)

        assert_record_equal(self, self.mapper.model2data(res), d)

    def test_with_artists_then_only_artists_loaded(self):
        artists = [ArtistRecord(name='pink floyd'), ArtistRecord(name='king crimson')]
        d = UserRecord(name='user', checked_artists=artists)
        res = self.mapper.data2model(d)
        self.assertEqual(len(res._checked_artists), len(artists))
        for data, model in zip(artists, res._checked_artists):
            self.assertEqual(data.name, model.name)
        self.assertIsNone(res._oauth_tokens)

        assert_record_equal(self, self.mapper.model2data(res), d)

    def test_with_oauth_tokens_then_only_oauth_tokens_loaded(self):
        tokens = [OauthTokenRecord(access_token='token1', access_secret='secret1', user_id=1, provider_type=1),
                  OauthTokenRecord(access_token='token2', access_secret='secret2', user_id=1, provider_type=2)]
        d = UserRecord(name='user', oauth_tokens=tokens)
        res = self.mapper.data2model(d)
        self.assertIsNone(res._checked_artists)
        self.assertEqual(len(res._oauth_tokens), len(tokens))
        for data, model in zip(tokens, res._oauth_tokens):
            self.assertEqual(data.provider_type, model.provider.type_num)

        assert_record_equal(self, self.mapper.model2data(res), d)


class TestUserRepository(DBTestCaseBase):

    def test_insert_user(self):
        u = User(name='hoge')
        user_repository.save(u)

        um = user_repository.find_by_name('hoge')

        record = UserRecord.query.get(um.id)
        self.assertEqual(u.id, record.id)
        self.assertEqual(u.name, record.name)

    def test_update_user(self):
        self.test_insert_user()

        um = user_repository.find_by_name('hoge')
        um._name = 'fuga'
        user_repository.save(um)

        record = UserRecord.query.get(um.id)
        self.assertEqual(record.name, 'fuga')
