#!/usr/bin/python

import csv
import sys
import pprint
import collections
import difflib

COMPANY = 'Company/Affiliation'
NAME = 'Name'
MEMBER = 'Are you or your company a RISC-V Foundation member?'
RANK = 'Rank the debug proposals. Put the proposal you like best in first place, second best in second place, and so on.'
COMMENT = 'Comments'

def header(title, dash='-'):
    if title:
        dashes = dash * (36 - len(title))
        before = dashes[:len(dashes)/2]
        after = dashes[len(dashes)/2:]
        print "%s[ %s ]%s" % (before, title, after)
    else:
        print dash * 40

def summarize(results):
    rankings = collections.Counter(r[RANK] for r in results).items()
    rankings.sort(key=lambda x: x[1], reverse=True)
    for order, count in rankings:
        print "%3d  %s" % (count, order)

def main():
    print "= RISC-V Debug System Preliminary Poll Results"
    print "Tim Newsome <tim@sifive.com>"
    print

    reader = csv.reader(file("results.csv"))
    headers = reader.next()
    results = []
    seen_companies = set()
    for row in reader:
        result = {k: v for k, v in zip(headers, row)}

        # Fixes go here
        if result[NAME] == "Krste Asanovic":
            # Krste wants to vote UC Berkeley
            result[COMPANY] = "UC Berkeley Architecture Research"
        # End of fixes

        if result[COMPANY] == "test":
            print "Skipping submission from %s (%s)" % (result[NAME],
                    result[COMPANY])
            continue

        similar_companies = difflib.get_close_matches(result[COMPANY], seen_companies)
        if similar_companies:
            print "Skipping vote for %s (by %s). It's probably a second vote for %s" % (
                    result[COMPANY], result[NAME], similar_companies[0])
            continue
        seen_companies.add(result[COMPANY])

        results.append(result)

    print
    print "== Results from RISC-V members"
    print
    member_results = [r for r in results if r[MEMBER] == "yes"]
    summarize(member_results)
    print
    print "Votes from %s." % (", ".join(sorted(r[COMPANY] for r in member_results)))

    print
    print "== Overall results"
    print
    summarize(results)

    print
    print "Votes from %s." % (", ".join(sorted(r[NAME] for r in results)))

    print
    print "== Comments"
    print
    for r in results:
        if r[COMMENT]:
            print "[quote, %s (%s)]" % (r[NAME], r[COMPANY])
            print "____"
            print r[COMMENT]
            print "____"

sys.exit(main())
