# -*- coding: utf-8 -*-

from robotstxt import parse, TestAgent

def test_parse_1():
    testdata = ['User-agent: *',
                'Disallow: /']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == False
    assert t.can_fetch('*', '/allow.html') == False
    assert t.can_fetch('Googlebot', '/allow.html') == False
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_2():
    testdata = ['User-agent: *',
                'Disallow:']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == True
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == True
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_3():
    testdata = ['User-agent: *',
                'Allow: /']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == True
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == True
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_4():
    testdata = ['User-agent: Googlebot',
                'Allow: /']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == True
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == True
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_5():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Allow: /']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == True
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == True
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_6():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == False
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == True
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_7():
    testdata = ['User-agent: Googlebot',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == False
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == True
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_8():
    testdata = ['User-agent: Googlebot',
                'Disallow: /',
                'User-agent: *',
                'Disallow: /',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == False
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == False
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_9():
    testdata = ['User-agent: Googlebot',
                'Disallow: /',
                '# default',
                'User-agent: *',
                'Disallow: / # all',
                'Allow: /allow.html',
                'Sitemap: https://www.example.com/sitemap.xml']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == False
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == False
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_10():
    testdata = ['# default',
                'Disallow: / # all',
                'Allow: /allow.html']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/') == False
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/allow.html') == True
    assert t.can_fetch('*', 'http://example.com/') == False

def test_parse_11():
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
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('Googlebot', '/') == True
    assert t.can_fetch('Googlebot', '/allow.html') == True
    assert t.can_fetch('Googlebot', '/disallow.html') == False
    assert t.can_fetch('Googlebot', '/disallow.html?') == True
    assert t.can_fetch('Googlebot', '/search?q=') == False
    assert t.can_fetch('Googlebot', '/search?q=a') == False
    assert t.can_fetch('Googlebot', '/search?q=a&x=b') == True
    assert t.can_fetch('*', '/allow.html') == True
    assert t.can_fetch('*', '/allow.html?a=b') == True

def test_parse_12():
    testdata = ['User-agent: *',
                'Disallow: /a',
                'Allow: /a/b',
                'Disallow: /a/b',
                'Allow: /a/b/c',
                'Disallow: /a/b/c']
    r = parse(testdata)
    t1 = TestAgent('https://www.example.com/', r, 1)
    t2 = TestAgent('https://www.example.com/', r, 2)
    t3 = TestAgent('https://www.example.com/', r, 3)
    assert t1.can_fetch('*', '/a/b/c') == True
    assert t2.can_fetch('*', '/a/b/c') == False
    assert t3.can_fetch('*', '/a/b/c') == True

def test_parse_13():
    testdata = ['User-agent: *',
                'Disallow: /あ.html',
                'Disallow: /う.html$',
                'Disallow: /え.html?',
                'Allow: /え.html?名前=*']
    r = parse(testdata)
    t = TestAgent('https://www.example.com/', r)
    assert t.can_fetch('*', '/あ.html') == False
    assert t.can_fetch('*', '/%E3%81%82.html') == False
    assert t.can_fetch('*', '/い.html') == True
    assert t.can_fetch('*', '/う.html') == False
    assert t.can_fetch('*', '/え.html?年齢=不詳') == False
    assert t.can_fetch('*', '/え.html?名前=なまえ') == True
