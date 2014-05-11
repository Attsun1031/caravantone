# -*- coding: utf-8 -*-
from caravantone.testing import TestCaseBase, setup4testing
setup4testing()
import caravantone.model.oauth as oauth


class TestOauthToken(TestCaseBase):

    def test_init_with_valid_provider_type_then_created(self):
        o = oauth.OauthToken(access_token='access', access_secret='secret', provider_type=oauth.Provider.twitter.type_num)
        self.assertEqual(o.provider, oauth.Provider.twitter)

    def test_init_with_invalid_provider_type_then_raise_value_error(self):
        with self.assertRaises(ValueError):
            oauth.OauthToken(access_token='access', access_secret='secret', provider_type=10000)
