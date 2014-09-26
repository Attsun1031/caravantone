# -*- coding: utf-8 -*-
from caravantone.resources import UserResource
from caravantone.testing import IntegrationTestBase, DummyRequest
from caravantone.dao import UserRecord, ArtistRecord, db_session
from caravantone.view.user import add_artist


class TestRegisterArtistAPI(IntegrationTestBase):
    """
    test register artist api
    """

    def setUp(self):
        super(TestRegisterArtistAPI, self).setUp()
        self.user = UserRecord(name='test_user')
        self.artist = ArtistRecord(name='pink floyd', freebase_topic_id='/music/pink_floyd')
        db_session.add_all([self.user, self.artist])
        db_session.commit()
        self.config.testing_securitypolicy(userid='{user.id:d}:{user.name}'.format(user=self.user))

    def test_when_register_artist_not_registered_then_created(self):
        # setup
        req = DummyRequest(params=dict(name='Omer Klein', freebase_topic_id='/music/omer_klein'))
        ctx = UserResource(self.user.id)

        # exercise & verify
        res = add_artist(ctx, req)
        self.assertEqual(res, {'name': 'Omer Klein'})

    def test_when_register_artist_already_registered_then_not_created(self):
        # setup
        req = DummyRequest(params=dict(name='pink floyd', freebase_topic_id='/music/pink_floyd'))
        ctx = UserResource(self.user.id)

        # exercise & verify
        res = add_artist(ctx, req)
        self.assertEqual(res, {'name': 'pink floyd'})

        user = UserRecord.query.get(self.user.id)
        self.assertEqual(user.checked_artists[0].name, 'pink floyd')
        self.assertEqual(len(ArtistRecord.query.all()), 1)


if __name__ == '__main__':
    import unittest
    unittest.main()
