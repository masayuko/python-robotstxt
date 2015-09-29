# -*- coding: utf-8 -*-
from .baseobject import RobotsTxt, Ruleset
import re

RE = re.compile("(allow|disallow|user[-]?agent|sitemap|crawl-delay):[ \t]*(.*)", re.IGNORECASE)


def parse(lines):
    robotstxt = RobotsTxt()
    previous_line_was_a_user_agent = False
    current_ruleset = None
    for line in lines:

        # Remove comments
        line = line.partition('#')[0]
        line = line.strip()

        if not line:
            continue

        # Each non-empty line falls into one of six categories:
        # 1) User-agent: blah blah blah
        # 2) Disallow: blah blah blah
        # 3) Allow: blah blah blah
        # 4) Crawl-delay: blah blah blah
        # 5) Sitemap: blah blah blah
        # 6) Everything else
        # 1 - 5 are interesting and I find them with the regex 
        # below. Category 6 I discard as directed by the MK1994 
        # ("Unrecognised headers are ignored.")
        # Note that 4 & 5 are specific to GYM2008 syntax, but 
        # respecting them here is not a problem. They're just 
        # additional information the caller is free to ignore.
        matches = RE.findall(line)

        if not matches:
            # Ignore this line
            continue

        field, data = matches[0]
        field = field.lower()
        data = data.replace('\t', ' ').strip()

        if field in ('useragent', 'user-agent', '-agent') and data:
            if previous_line_was_a_user_agent:
                current_ruleset.add_robot_name(data)
            else:
                current_ruleset = Ruleset()
                current_ruleset.add_robot_name(data)
                robotstxt.rulesets.append(current_ruleset)
            previous_line_was_a_user_agent = True
        elif field == 'allow' and data:
            if not current_ruleset:
                current_ruleset = Ruleset()
                current_ruleset.add_robot_name('*')
                robotstxt.rulesets.append(current_ruleset)
            current_ruleset.add_allow_rule(data)
            previous_line_was_a_user_agent = False
        elif field == 'sitemap' and data:
            robotstxt.sitemaps.append(data)
            previous_line_was_a_user_agent = False
        elif field == 'crawl-delay' and data:
            try:
                crawl_delay = float(data)
                if not current_ruleset:
                    current_ruleset = Ruleset()
                    current_ruleset.add_robot_name('*')
                    robotstxt.rulesets.append(current_ruleset)
                current_ruleset.crawl_delay = crawl_delay
            except ValueError:
                # Invalid crawl-delay -- Ignore
                pass
            previous_line_was_a_user_agent = False
        else: # disallow
            if not current_ruleset:
                current_ruleset = Ruleset()
                current_ruleset.add_robot_name('*')
                robotstxt.rulesets.append(current_ruleset)
            current_ruleset.add_disallow_rule(data)
            previous_line_was_a_user_agent = False

    return robotstxt
