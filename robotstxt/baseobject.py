# -*- coding: utf-8 -*-
import urilib


class RobotsTxt(object):
    """ RobotsTxt represents a set of Ruleset and sitemaps """
    def __init__(self):
        self.rulesets = []
        self.sitemaps = []

    def add_ruleset(self, ruleset):
        self.rulesets.append(ruleset)

    def add_sitemap(self, sitemap):
        self.sitemaps.append(sitemap)


class Ruleset(object):
    """ Ruleset represents a set of allow/disallow rules (and possibly a
    crawl delay) that apply to a set of user agents.

    """
    def __init__(self):
        self.robot_names = []
        self.rules = []
        self.crawl_delay = None

    def add_robot_name(self, bot):
        self.robot_names.append(bot)

    def add_rule(self, allow, path):
        self.rules.append((allow, path))

    def add_allow_rule(self, path):
        self.rules.append((True, path))

    def add_disallow_rule(self, path):
        self.rules.append((False, path))

    def add_sitemap(self, path):
        self.sitemaps.append(path)


def encode_path(path):
    splited = urilib.urisplit(path)
    epath = urilib.uriencode(splited.path, safe='/$*?=&;@,#')
    if splited.query:
        query = urilib.uriencode_plus(splited.query, safe='/$*?=&;@,#')
        path = epath + '?' + query
    else:
        if path[-1] == '?':
            path = epath + '?'
        else:
            path = epath
    return path
