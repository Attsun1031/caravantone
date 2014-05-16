# -*- coding: utf-8 -*-
from flask.json import loads
import caravantone.testing as testing
testing.setup4testing()

from caravantone.dao import UserRecord, db_session


class TestArtistAPI(testing.AppTestBase):

    def _setUp(self):
        self.u = UserRecord(name='test_user')
        db_session.add(self.u)
        db_session.commit()

    def test_when_register_artist_not_registered_then_created(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            rv = self.app.post('/artists', data=dict(name='Omer Klein', freebase_topic_id='/music/omer_klein'))
        self.assertEqual(loads(rv.data.decode('utf8'))['name'], 'Omer Klein')

        user = UserRecord.query.get(self.u.id)
        self.assertEqual(user.checked_artists[0].name, 'Omer Klein')
        self.assertEqual(user.checked_artists[0].freebase_topic_id, '/music/omer_klein')
