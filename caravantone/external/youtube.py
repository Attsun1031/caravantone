# -*- coding: utf-8 -*-

"""API client for youtube"""

import json
import requests
from werkzeug.utils import cached_property

from caravantone.app import app
from caravantone.dao import redis_session


youtube_api = 'https://www.googleapis.com/youtube/v3/search?part=id,snippet&q={}&key={}&order=date&type=video'

one_day = 60 * 60 * 24


def search(keyword, cache_expiration=one_day, ignore_cache=False):
    """Search videos from youtube by keyword.
    Result is cached on Redis for cache_expiration sec.

    :param str keyword: search query
    :param int cache_expiration: expiration sec for cache
    :param bool ignore_cache: ignore cache?
    :return: Youtube Video objects (iterator)
    :rtype: (YoutubeVideo)
    """
    if not keyword.strip():
        raise ValueError('Empty keyword')

    key = '{}:{}'.format('youtube_search', keyword)
    cache = redis_session.get(key)
    if cache is None or ignore_cache:
        res = requests.get(youtube_api.format(keyword, app.config['YOUTUBE_DEVELOPER_KEY']))
        content = json.loads(res.content.decode('utf8'))
        items = content['items']
        redis_session.setex(key, cache_expiration, json.dumps(items))
    else:
        items = json.loads(cache.decode('utf8'))
    yield from map(YoutubeVideo, items)


class YoutubeVideo(object):
    """Container object for information about youtube video"""

    video_url_template = 'https://www.youtube.com/watch?v={}'

    def __init__(self, item_data):
        self.__item_data = item_data

    @property
    def item_data(self):
        return self.__item_data

    @cached_property
    def video_id(self):
        return self.item_data['id']['videoId']

    @cached_property
    def title(self):
        return self.item_data['snippet']['title']

    @cached_property
    def video_url(self):
        return self.video_url_template.format(self.video_id)


if __name__ == '__main__':
    for item in search('上原ひろみ'):
        print(item.item_data)
        print(item.title, item.video_url)
