# -*- coding: utf-8 -*-
import caravantone.testing as testing
testing.setup4testing()

from caravantone.dao import UserRecord, db_session


class TestLoginCheck(testing.AppTestBase):

    def _setUp(self):
        self.u = UserRecord(name='test_user')
        db_session.add(self.u)
        db_session.commit()

    def test_when_user_id_not_in_session_then_abort(self):
        with self.app as c:
            rv = c.post('/artists', data=dict(name='Omer Klein', freebase_topic_id='/music/omer_klein'))

        self.assertEqual(rv.status, '400 BAD REQUEST')

    def test_when_user_not_found_then_abort(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2
            rv = c.post('/artists', data=dict(name='Omer Klein', freebase_topic_id='/music/omer_klein'))

        self.assertEqual(rv.status, '400 BAD REQUEST')


if __name__ == '__main__':
    import unittest
    unittest.main()
