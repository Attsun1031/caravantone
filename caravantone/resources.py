# -*- coding: utf-8 -*-


def link(parent, child):
    parent[child.__name__] = child
    child.__parent__ = parent


class MyRootResource(dict):
    __name__ = __parent__ = None


class PathResource(object):
    __name__ = 'path'


root = MyRootResource()
link(root, PathResource())


def root_factory(request):
    return root


# TODO: aritsts APIをリソースで引けるようにする。
# http://zaiste.net/2013/12/building_a_restful_api_with_pyramid_resource_and_traversal/
# http://www.slideshare.net/aodag/pyramid-39068836
# http://pelican.aodag.jp/20140205-pyramid-controller-style.html
# http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/traversal.html
# http://docs.pylonsproject.jp/projects/pyramid-doc-ja/en/latest/narr/resources.html
