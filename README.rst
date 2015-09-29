=========
robotstxt
=========

A robots.txt manipulation library for Python.

Features
========

* Wildcard matching (* and $)
* Support for Sitemaps
* Support for Crawl-delay

Usage
=====

.. code-block:: python

   from robotstxt import parse, TestAgent

   testdata = ['User-agent: Googlebot',
               'Disallow: /',
               'User-agent: *',
               'Disallow: /',
               'Allow: /allow.html',
               'Sitemap: https://www.example.com/sitemap.xml']
   robotstxt = parse(testdata)
   agent = TestAgent('https://www.example.com/', robotstxt)
   result = agent.can_fetch('*', '/allow.html')
