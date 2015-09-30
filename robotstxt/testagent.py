# -*- coding: utf-8 -*-
import re
import urilib
from unicodedata import normalize as unicodenormalize
from .baseobject import encode_path

class TestAgent(object):
    """ Test Agent """
    def __init__(self, base, robotstxt, method=1):
        self.rulesets = []
        self.default = None
        for ruleset in robotstxt.rulesets:
            fortest = RulesetForTest(ruleset, method)
            self.rulesets.append(fortest)
            if '*' in ruleset.robot_names:
                self.default = fortest
        self.base = base
        self.method = method
        self.cached = dict()

    def can_fetch(self, useragent, url):
        if isinstance(url, bytes):
            SLASH = b'/'
            Q = b'?'
        else:
            SLASH = '/'
            Q= '?'

        splitted = urilib.urisplit(url)
        userinfo = splitted.getuserinfo()
        if userinfo:
            userinfo = _unicodenormalize(userinfo)
        urlbase = urilib.uricompose(
            scheme=splitted.getscheme(),
            userinfo=userinfo,
            host=splitted.gethost(),
            port=splitted.getport(),
            path=SLASH)
        if urlbase != SLASH and self.base != urlbase:
            # don't have to do with this
            return False

        target = self.cached.get(useragent, None)
        if not target:
            for ruleset in self.rulesets:
                if ruleset.does_user_agent_match(useragent):
                    target = ruleset
                    self.cached[useragent] = target
                    break

        if useragent != '*' and not target:
            target = self.default

        if target:
            path = splitted.getpath()
            if path:
                path = _unicodenormalize(path)
            query = splitted.query
            if query:
                qsl = urilib.querylist(_unicodenormalize(query))
            else:
                qsl = None

            norm = urilib.uricompose(path=path, query=qsl)

            if url[-1] == Q:
                norm = norm + Q

            return target.is_url_allowed(norm, self.method)

        return True


class RulesetForTest(object):
    """ Ruleset for Test """
    def __init__(self, original, method=1):
        self.original = original
        self.rules = []
        for rule in original.rules:
            if rule[0]:
                # Allow
                if rule[1]:
                    self.rules.append((True, rule[1],
                                       re.compile(self._getpattern(rule[1]))))
            else:
                # Disallow
                if rule[1]:
                    self.rules.append((False, rule[1],
                                       re.compile(self._getpattern(rule[1]))))
                else:
                    self.rules.append((True, '/', re.compile(r'^/.*')))

        if method == 3:
            self.rules = sorted(self.rules, key=lambda x: len(x[1]),
                                reverse=True)

    def _getpattern(self, path):
        path = encode_path(path)
        if path[-1] == '$':
            appendix = r'$'
            path = path[:-1]
        else:
            appendix = r'.*'
        if '*' in path:
            parts = path.split('*')
            pattern = r'.*'.join([re.escape(p) for p in parts])
        else:
            pattern = re.escape(path)
        return r'^' + pattern + appendix

    def does_user_agent_match(self, useragent):
        for name in self.original.robot_names:
            if name.split('/')[0].lower() == useragent.lower():
                return True
        return False

    def is_url_allowed(self, path, method=1):
        return _is_url_allowed(self.rules, path, method)


def _unicodenormalize(ustr, method='NFC'):
    if isinstance(ustr, bytes):
        return unicodenormalize(method, ustr.decode('utf-8')).encode('utf-8')
    else:
        return unicodenormalize(method, ustr)


def _is_url_allowed(rules, path, method=1):
    allowed = True
    if method == 1:
        for rule in rules:
            if rule[2].match(path):
                if rule[0]:
                    allowed = True
                    break
                else:
                    allowed = False
    elif method == 2:
        for rule in rules:
            if rule[2].match(path):
                if rule[0]:
                    allowed = True
                else:
                    allowed = False
    elif method == 3:
        for rule in rules:
            if rule[2].match(path):
                if rule[0]:
                    allowed = True
                else:
                    allowed = False
                break
    return allowed
