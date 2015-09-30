# -*- coding: utf-8 -*-

from robotstxt import parse, dumps

def test_parse_1():
    testdata = ['User-agent: *',
                'Disallow: /']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: *\nDisallow: /\n'

def test_parse_2():
    testdata = ['User-agent: *',
                'Disallow:']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: *\nDisallow:\n'
    d = dumps(r, ordered=True)
    assert d == 'User-agent: *\nAllow: /\n'

def test_parse_3():
    testdata = ['User-agent: *',
                'Allow: /']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: *\nAllow: /\n'

def test_parse_4():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Allow: /']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: Googlebot\nUser-agent: *\nAllow: /\n'

def test_parse_5():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: Googlebot\nUser-agent: *\nDisallow: /\nAllow: /allow.html\n'
    d = dumps(r, ordered=True)
    assert d == 'User-agent: Googlebot\nUser-agent: *\nDisallow: /\nAllow: /allow.html\n'

def test_parse_6():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: Googlebot\nUser-agent: *\nDisallow: /\nAllow: /allow.html\nSitemap: https://www.example.com/sitemap.xml\n'

def test_parse_7():
    testdata = ['User-agent: Googlebot',
                'Disallow: /',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: Googlebot\nDisallow: /\nUser-agent: *\nDisallow: /\nAllow: /allow.html\nSitemap: https://www.example.com/sitemap.xml\n'

def test_parse_8():
    testdata = ['User-agent: Googlebot',
                'Disallow: /',
                '# default',
                'User-agent: *',
                'Disallow: / # all',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: Googlebot\nDisallow: /\nUser-agent: *\nDisallow: /\nAllow: /allow.html\nSitemap: https://www.example.com/sitemap.xml\n'

def test_parse_9():
    testdata = ['# default',
                'Disallow: / # all',
                'Allow: /allow.html',
                'Crawl-delay: 1']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: *\nDisallow: /\nAllow: /allow.html\nCrawl-delay: 1\n'

def test_parse_10():
    testdata = ['User-agent: Googlebot',
                'Disallow: /disallow.html$',
                'Allow: /allow.html$',
                'Disallow: /search?q=',
                'Allow: /search?q=*&*$',
                'User-agent: *',
                'Disallow: /',
                'Allow: /test/',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: Googlebot\nDisallow: /disallow.html$\nAllow: /allow.html$\nDisallow: /search?q=\nAllow: /search?q=*&*$\nUser-agent: *\nDisallow: /\nAllow: /test/\nAllow: /allow.html\nSitemap: https://www.example.com/sitemap.xml\n'
    d = dumps(r, ordered=True)
    assert d == 'User-agent: Googlebot\nDisallow: /search?q=\nDisallow: /disallow.html$\nAllow: /allow.html$\nAllow: /search?q=*&*$\nUser-agent: *\nDisallow: /\nAllow: /test/\nAllow: /allow.html\nSitemap: https://www.example.com/sitemap.xml\n'

def test_parse_11():
    testdata = ['User-agent: *',
                'Disallow: /a',
                'Allow: /a/b',
                'Disallow: /a/b',
                'Allow: /a/b/c',
                'Disallow: /a/b/c']
    r = parse(testdata)
    d = dumps(r)
    assert d == 'User-agent: *\nDisallow: /a\nAllow: /a/b\nDisallow: /a/b\nAllow: /a/b/c\nDisallow: /a/b/c\n'
    d = dumps(r, ordered=True)
    assert d == 'User-agent: *\nDisallow: /a\nDisallow: /a/b\nDisallow: /a/b/c\nAllow: /a/b\nAllow: /a/b/c\n'

def test_parse_12():
    testdata = [u'User-agent: *',
                u'Disallow: /あ.html',
                u'Disallow: /う.html$',
                u'Disallow: /え.html?',
                u'Allow: /え.html?名前=*']
    r = parse(testdata)
    d = dumps(r)
    assert d == u'User-agent: *\nDisallow: /%E3%81%82.html\nDisallow: /%E3%81%86.html$\nDisallow: /%E3%81%88.html?\nAllow: /%E3%81%88.html?%E5%90%8D%E5%89%8D=*\n'
    d = dumps(r, asis=True)
    print(d)
    assert d == u'User-agent: *\nDisallow: /あ.html\nDisallow: /う.html$\nDisallow: /え.html?\nAllow: /え.html?名前=*\n'

def test_parse_13():
    testdata = [u'User-agent: *',
                u'Disallow: /あ.html',
                u'Disallow: /う.html$',
                u'Allow: /え.html?名前=*',
                u'Disallow: /え.html?',]
    r = parse(testdata)
    d = dumps(r)
    assert d == u'User-agent: *\nDisallow: /%E3%81%82.html\nDisallow: /%E3%81%86.html$\nAllow: /%E3%81%88.html?%E5%90%8D%E5%89%8D=*\nDisallow: /%E3%81%88.html?\n'
    d = dumps(r, ordered=True)
    assert d == u'User-agent: *\nDisallow: /%E3%81%82.html\nDisallow: /%E3%81%86.html$\nDisallow: /%E3%81%88.html?\nAllow: /%E3%81%88.html?%E5%90%8D%E5%89%8D=*\n'
    d = dumps(r, asis=True)
    print(d)
    assert d == u'User-agent: *\nDisallow: /あ.html\nDisallow: /う.html$\nAllow: /え.html?名前=*\nDisallow: /え.html?\n'
    d = dumps(r, asis=True, ordered=True)
    print(d)
    assert d == u'User-agent: *\nDisallow: /あ.html\nDisallow: /う.html$\nDisallow: /え.html?\nAllow: /え.html?名前=*\n'

def test_parse_14():
    testdata = [u'User-agent: *',
                u'Disallow: /あ.html',
                u'Disallow: /う.html$',
                u'Disallow: /え.html?',
                u'Allow: /え.html?名前=*',
                u'Sitemap: https://例.com/サイトマップ.xml']
    r = parse(testdata)
    d = dumps(r)
    assert d == u'User-agent: *\nDisallow: /%E3%81%82.html\nDisallow: /%E3%81%86.html$\nDisallow: /%E3%81%88.html?\nAllow: /%E3%81%88.html?%E5%90%8D%E5%89%8D=*\nSitemap: https://xn--fsq.com/%E3%82%B5%E3%82%A4%E3%83%88%E3%83%9E%E3%83%83%E3%83%97.xml\n'
    d = dumps(r, asis=True)
    print(d)
    assert d == u'User-agent: *\nDisallow: /あ.html\nDisallow: /う.html$\nDisallow: /え.html?\nAllow: /え.html?名前=*\nSitemap: https://例.com/サイトマップ.xml\n'
