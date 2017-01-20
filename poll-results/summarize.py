#!/usr/bin/python

import csv
import sys
import pprint
import collections
import difflib
# https://github.com/bradbeattie/python-vote-core
import pyvotecore

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

def summarize(name, results, field):
    print
    print "== Results from %s" % name
    print
    print "Votes from %s." % (", ".join(sorted(r[field] for r in results)))
    print

    rankings = collections.Counter(r[RANK] for r in results).items()
    rankings.sort(key=lambda x: x[1], reverse=True)
    ballots = []
    for order, count in rankings:
        print "%3d  %s" % (count, order)
        ballots.append({"count": count, "ballot": [[x] for x in order.split(",")]})

    from pyvotecore.schulze_method import SchulzeMethod
    from pyvotecore.condorcet import CondorcetHelper
    schulze = SchulzeMethod(ballots, ballot_notation=CondorcetHelper.BALLOT_NOTATION_GROUPING)

    print
    if hasattr(schulze, "tied_winners"):
        print "*Schulze winners: tie between %s*" % (", ".join(schulze.tied_winners))
    else:
        print "*Schulze winner: %s*" % schulze.winner

    print
    print "Algorithm details:"
    print "```"
    pprint.pprint(schulze.as_dict())
    print "```"

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
        if result[NAME] == "Adam Husar":
            # Adam votes for Codasip
            result[COMPANY] = "Codasip"
        if result[NAME] == "Jiri Bartak":
            # Adam already voted for Codasip. Jiri can vote for himself.
            result[COMPANY] = result[NAME]
            result[MEMBER] = "no"
        if result[NAME] == "Po-wei Huang":
            # Po-wei is an individual member. They don't have voting rights in
            # the foundation. (I should have made this more clear up front.)
            result[MEMBER] = "no"
        # End of fixes

        if result[COMPANY] == "test":
            continue

        similar_companies = difflib.get_close_matches(result[COMPANY], seen_companies)
        if similar_companies:
            print "Skipping vote for %s (by %s). It's probably a second vote for %s" % (
                    result[COMPANY], result[NAME], similar_companies[0])
            continue
        seen_companies.add(result[COMPANY])

        results.append(result)

    member_results = [r for r in results if r[MEMBER] == "yes"]
    summarize("Voting RISC-V members", member_results, COMPANY)

    other_results = [r for r in results if r[MEMBER] == "no"]
    summarize("Everybody Else", other_results, NAME)

    summarize("Both Groups Combined", results, NAME)

    print
    print "== Comments"
    print
    for r in results:
        if r[COMMENT]:
            print "[quote, %s (%s)]" % (r[NAME], r[COMPANY])
            print "____"
            print r[COMMENT]
            print "____"
            print

sys.exit(main())
