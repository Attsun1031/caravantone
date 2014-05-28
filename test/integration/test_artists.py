# -*- coding: utf-8 -*-
from flask.json import loads
import caravantone.testing as testing
testing.setup4testing()

from caravantone.dao import UserRecord, ArtistRecord, db_session


class TestArtistAPI(testing.AppTestBase):

    def _setUp(self):
        self.user = UserRecord(name='test_user')
        self.artist = ArtistRecord(name='pink floyd', freebase_topic_id='/music/pink_floyd')
        db_session.add_all([self.user, self.artist])
        db_session.commit()

    def test_when_register_artist_not_registered_then_created(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            rv = c.post('/artists', data=dict(name='Omer Klein', freebase_topic_id='/music/omer_klein'))
        self.assertEqual(loads(rv.data.decode('utf8'))['name'], 'Omer Klein')

        user = UserRecord.query.get(self.user.id)
        self.assertEqual(user.checked_artists[0].name, 'Omer Klein')
        self.assertEqual(user.checked_artists[0].freebase_topic_id, '/music/omer_klein')

    def test_when_register_artist_already_registered_then_not_created(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            rv = c.post('/artists', data=dict(name='pink floyd', freebase_topic_id='/music/pink_floyd'))
        self.assertEqual(loads(rv.data.decode('utf8'))['name'], 'pink floyd')

        user = UserRecord.query.get(self.user.id)
        self.assertEqual(user.checked_artists[0].name, 'pink floyd')
        self.assertEqual(len(ArtistRecord.query.all()), 1)


if __name__ == '__main__':
    import unittest
    unittest.main()
