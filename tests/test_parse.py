# -*- coding: utf-8 -*-
import pytest

from robotstxt import parse

def test_parse_1():
    testdata = ['User-agent: *',
                'Disallow: /']
    r = parse(testdata)
    assert len(r.rulesets) == 1
    assert len(r.rulesets[0].robot_names) == 1
    assert r.rulesets[0].robot_names[0] == '*'
    assert len(r.rulesets[0].rules) == 1
    assert r.rulesets[0].rules[0] == (False, '/')
    assert len(r.sitemaps) == 0

def test_parse_2():
    testdata = ['User-agent: *',
                'Disallow:']
    r = parse(testdata)
    assert len(r.rulesets) == 1
    assert len(r.rulesets[0].robot_names) == 1
    assert r.rulesets[0].robot_names[0] == '*'
    assert len(r.rulesets[0].rules) == 1
    assert r.rulesets[0].rules[0] == (False, '')
    assert len(r.sitemaps) == 0

def test_parse_3():
    testdata = ['User-agent: *',
                'Allow: /']
    r = parse(testdata)
    assert len(r.rulesets) == 1
    assert len(r.rulesets[0].robot_names) == 1
    assert r.rulesets[0].robot_names[0] == '*'
    assert len(r.rulesets[0].rules) == 1
    assert r.rulesets[0].rules[0] == (True, '/')
    assert len(r.sitemaps) == 0

def test_parse_4():
    testdata = ['User-agent: Googlebot',
                'Allow: /']
    r = parse(testdata)
    assert len(r.rulesets) == 1
    assert len(r.rulesets[0].robot_names) == 1
    assert r.rulesets[0].robot_names[0] == 'Googlebot'
    assert len(r.rulesets[0].rules) == 1
    assert r.rulesets[0].rules[0] == (True, '/')
    assert len(r.sitemaps) == 0

def test_parse_5():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Allow: /']
    r = parse(testdata)
    assert len(r.rulesets) == 1
    assert len(r.rulesets[0].robot_names) == 2
    assert r.rulesets[0].robot_names[0] == 'Googlebot'
    assert r.rulesets[0].robot_names[1] == '*'
    assert len(r.rulesets[0].rules) == 1
    assert r.rulesets[0].rules[0] == (True, '/')
    assert len(r.sitemaps) == 0

def test_parse_6():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html']
    r = parse(testdata)
    assert len(r.rulesets) == 1
    assert len(r.rulesets[0].robot_names) == 2
    assert r.rulesets[0].robot_names[0] == 'Googlebot'
    assert r.rulesets[0].robot_names[1] == '*'
    assert len(r.rulesets[0].rules) == 2
    assert r.rulesets[0].rules[0] == (False, '/')
    assert r.rulesets[0].rules[1] == (True, '/allow.html')
    assert len(r.sitemaps) == 0

def test_parse_7():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    assert len(r.rulesets) == 1
    assert len(r.rulesets[0].robot_names) == 2
    assert r.rulesets[0].robot_names[0] == 'Googlebot'
    assert r.rulesets[0].robot_names[1] == '*'
    assert len(r.rulesets[0].rules) == 2
    assert r.rulesets[0].rules[0] == (False, '/')
    assert r.rulesets[0].rules[1] == (True, '/allow.html')
    assert len(r.sitemaps) == 1
    assert r.sitemaps[0] == 'https://www.example.com/sitemap.xml'

def test_parse_8():
    testdata = ['User-agent: Googlebot',
                'Disallow: /',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    assert len(r.rulesets) == 2
    assert len(r.rulesets[0].robot_names) == 1
    assert r.rulesets[0].robot_names[0] == 'Googlebot'
    assert len(r.rulesets[0].rules) == 1
    assert r.rulesets[0].rules[0] == (False, '/')
    assert len(r.rulesets[1].robot_names) == 1
    assert r.rulesets[1].robot_names[0] == '*'
    assert len(r.rulesets[1].rules) == 2
    assert r.rulesets[1].rules[0] == (False, '/')
    assert r.rulesets[1].rules[1] == (True, '/allow.html')
    assert len(r.sitemaps) == 1
    assert r.sitemaps[0] == 'https://www.example.com/sitemap.xml'

def test_parse_9():
    testdata = ['User-agent: Googlebot',
                'Disallow: /',
                '# default',
                'User-agent: *',
                'Disallow: / # all',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    assert len(r.rulesets) == 2
    assert len(r.rulesets[0].robot_names) == 1
    assert r.rulesets[0].robot_names[0] == 'Googlebot'
    assert len(r.rulesets[0].rules) == 1
    assert r.rulesets[0].rules[0] == (False, '/')
    assert len(r.rulesets[1].robot_names) == 1
    assert r.rulesets[1].robot_names[0] == '*'
    assert len(r.rulesets[1].rules) == 2
    assert r.rulesets[1].rules[0] == (False, '/')
    assert r.rulesets[1].rules[1] == (True, '/allow.html')
    assert len(r.sitemaps) == 1
    assert r.sitemaps[0] == 'https://www.example.com/sitemap.xml'

def test_parse_10():
    testdata = ['# default',
                'Disallow: / # all',
                'Allow: /allow.html']
    r = parse(testdata)
    assert len(r.rulesets) == 1
    assert len(r.rulesets[0].robot_names) == 1
    assert r.rulesets[0].robot_names[0] == '*'
    assert len(r.rulesets[0].rules) == 2
    assert r.rulesets[0].rules[0] == (False, '/')
    assert r.rulesets[0].rules[1] == (True, '/allow.html')
    assert len(r.sitemaps) == 0
