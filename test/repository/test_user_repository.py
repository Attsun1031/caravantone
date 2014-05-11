# -*- coding: utf-8 -*-
from caravantone.testing import setup4testing, TestCaseBase
setup4testing()
import caravantone.repository.user as user
from caravantone.repository.artist import ArtistMapper
from caravantone.dao import UserRecord, OauthTokenRecord, ArtistRecord


class TestUserMapperData2Model(TestCaseBase):

    def setUp(self):
        self.mapper = user.UserMapper(ArtistMapper(), user.OauthTokenMapper())

    def test_without_relation_then_no_relation_loaded(self):
        d = UserRecord(name='user')
        res = self.mapper.data2model(d)
        self.assertIsNone(res._checked_artists)
        self.assertIsNone(res._oauth_tokens)

    def test_with_artists_then_only_artists_loaded(self):
        artists = [ArtistRecord(name='pink floyd'), ArtistRecord(name='king crimson')]
        d = UserRecord(name='user', checked_artists=artists)
        res = self.mapper.data2model(d)
        self.assertEqual(len(res._checked_artists), len(artists))
        self.assertIsNone(res._oauth_tokens)

    def test_with_oauth_tokens_then_only_oauth_tokens_loaded(self):
        tokens = [OauthTokenRecord(user_id=1, provider_type=1), OauthTokenRecord(user_id=1, provider_type=2)]
        d = UserRecord(name='user', oauth_tokens=tokens)
        res = self.mapper.data2model(d)
        self.assertIsNone(res._checked_artists)
        self.assertEqual(len(res._oauth_tokens), len(tokens))


# TODO: model2dataのテストを書く
