# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .baseobject import RobotsTxt, Ruleset, encode_path
import io
import urilib

def dumps(robotstxt, asis=False, ordered=False):
    fout = io.StringIO()
    dump(fout, robotstxt, asis, ordered)
    return fout.getvalue()


def _dump_rules(fout, rules, asis=False, ordered=False):
    for rule in rules:
        if rule[0] and rule[1]:
            if asis:
                path = rule[1]
            else:
                path = encode_path(rule[1])
            line = 'Allow: {0}\n'.format(path)
        elif not rule[0]:
            if rule[1]:
                if asis:
                    path = rule[1]
                else:
                    path = encode_path(rule[1])
                line = 'Disallow: {0}\n'.format(path)
            else:
                line = 'Disallow:\n'
        else:
            line = None
        if line:
            fout.write(line)


def _dump_ruleset(fout, ruleset, asis=False, ordered=False):
    for robot_name in ruleset.robot_names:
        fout.write('User-agent: {0}\n'.format(robot_name))

    if ordered:
        allows = []
        disallows = []
        for rule in ruleset.rules:
            if rule[0] and rule[1]:
                allows.append(rule)
            elif not rule[0]:
                if rule[1]:
                    disallows.append(rule)
                else:
                    allows.append((True, '/'))
        allows = sorted(allows, key=lambda x: len(x[1]))
        disallows = sorted(disallows, key=lambda x: len(x[1]))
        rules = disallows + allows
    else:
        rules = ruleset.rules
    _dump_rules(fout, rules, asis, ordered)

    if ruleset.crawl_delay:
        fout.write('Crawl-delay: {0:d}\n'.format(ruleset.crawl_delay))


def dump(fout, robotstxt, asis=False, ordered=False):
    for ruleset in robotstxt.rulesets:
        _dump_ruleset(fout, ruleset, asis, ordered)

    for sitemap in robotstxt.sitemaps:
        if not asis:
            sitemap = urilib.urinormalize(sitemap)
        fout.write('Sitemap: {0}\n'.format(sitemap))
