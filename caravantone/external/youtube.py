# -*- coding: utf-8 -*-

"""API client for youtube"""

import json
import requests

from caravantone.dao import redis_session


youtube_api = 'https://www.googleapis.com/youtube/v3/search?part=id,snippet&q={}&key={}&order=date&type=video'

one_day = 60 * 60 * 24


def search(keyword, cache_expiration=one_day, next_page_token='', ignore_cache=False):
    """Search videos from youtube by keyword.
    Result is cached on Redis for cache_expiration sec.

    :param str keyword: search query
    :param int cache_expiration: expiration sec for cache
    :param bool ignore_cache: ignore cache?
    :return: Youtube Video objects (iterator)
    :rtype: YoutubeSearchResult
    """
    if not keyword.strip():
        raise ValueError('Empty keyword')

    key = '{}:{}:{}'.format('youtube_search', next_page_token, keyword)
    cache = redis_session.get(key)
    if cache is None or ignore_cache:
        # url = youtube_api.format(keyword, app.config['YOUTUBE_DEVELOPER_KEY'])
        if next_page_token:
            url += '&pageToken={}'.format(next_page_token)
        res = requests.get(url)
        content = json.loads(res.content.decode('utf8'))
        result = YoutubeSearchResult.from_contents(content)
        redis_session.setex(key, cache_expiration, json.dumps(result.dumps()))
    else:
        content = json.loads(cache.decode('utf8'))
        result = YoutubeSearchResult.from_contents(content)
    return result


class YoutubeVideo(object):
    """Container object for information about youtube video"""

    video_url_template = 'https://www.youtube.com/watch?v={}'

    def __init__(self, item_data):
        self.__item_data = item_data

    @property
    def item_data(self):
        return self.__item_data

    # @cached_property
    def video_id(self):
        return self.item_data['id']['videoId']

    # @cached_property
    def title(self):
        return self.item_data['snippet']['title']

    # @cached_property
    def url(self):
        return self.video_url_template.format(self.video_id)

    # @cached_property
    def published_at(self):
        return self.item_data['snippet']['publishedAt']


class YoutubeSearchResult(object):
    """Search result of youtube API"""

    def __init__(self, items, next_page_token):
        self.__items = items
        self.__next_page_token = next_page_token

    @property
    def items(self):
        return self.__items

    @property
    def next_page_token(self):
        return self.__next_page_token

    def dumps(self):
        """Dump result data as dict
        Use this method to send result to different system or storage (cache or http response)

        :rtype: dict
        """
        return {'items': [v.item_data for v in self.items], 'nextPageToken': self.next_page_token}

    @classmethod
    def from_contents(cls, content):
        """Instantiate from youtube api result

        :param content: returned dict from youtube api
        """
        items = content['items']
        next_page_token = content.get('nextPageToken')
        return cls([YoutubeVideo(item) for item in items], next_page_token)


if __name__ == '__main__':
    result = search('上原ひろみ')
    print(result.next_page_token)
    for item in result.items:
        print(item.item_data)
        print(item.title, item.url)
