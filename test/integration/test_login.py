# -*- coding: utf-8 -*-

import unittest
from urllib.parse import urlparse
from caravantone.app import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_login(self):
        res = self.app.post('/login', data=dict(user='attsun', password='attsun'))
        assert urlparse(res.headers['Location']).path == '/'
        assert res.status_code == 302



if __name__ == '__main__':
    unittest.main()
