==================
python-openstates
==================

Python library for interacting with the Open State Project API.

The Open State Project provides data on state legislative activities,
including bill summaries, votes, sponsorships and state legislator
information.

python-openstates is a project of Sunlight Labs (c) 2011.
Written by Michael Stephens <mstephens@sunlightfoundation.com>.

Source: http://github.com/sunlightlabs/python-openstates

Requirements
============

python >= 2.4

remoteobjects >= 1.1

Installation
============

python-opentstates is available on PyPI and so it can most easily be
installed via ``pip install python-openstates`` or ``easy_install python-openstates``.

To install from a source distribution, run ``python setup.py install``.

Usage
=====

An API key can be obtained at http://services.sunlightlabs.com/.

Grab state metadata:

    >>> import openstates
    >>> openstates.API_KEY = 'YOUR_API_KEY_HERE'
    >>> ca = openstates.State.get('ca')
    >>> print ca.name
    California
    >>> print ca.lower_chamber_name
    Assembly
    >>> for term in ca.terms:
    ...     print term.name
    ...     for session in term.sessions:
    ...         print "Session: %s" % session
    20092010
    Session: 20092010
    Session: 20092010 Special Session 1
    Session: 20092010 Special Session 2
    Session: 20092010 Special Session 3
    Session: 20092010 Special Session 4
    Session: 20092010 Special Session 5
    Session: 20092010 Special Session 6
    Session: 20092010 Special Session 7
    Session: 20092010 Special Session 8

Lookup legislators by name:

    >>> mikes = openstates.Legislator.search(state='ca', first_name='Mike')
    >>> for mike in mikes:
    ...     print mike.full_name
    Duvall, Mike D.
    Gatto, Mike
    Eng, Mike
    Davis, Mike
    Feuer, Mike

Lookup legislators by name and party:

    >>> dem_mikes = openstates.Legislator.search(state='ca',
    ... party='Democratic', first_name='Mike')
    >>> for mike in dem_mikes:
    ...     print mike.full_name
    Gatto, Mike
    Eng, Mike
    Davis, Mike
    Feuer, Mike

Search bills:

    >>> bills = openstates.Bill.search('agriculture', state='vt')[0:3]
    >>> for bill in bills:
    ...     print "%s %s %s" % (bill.state, bill.bill_id, bill.title)
    vt H.0554 AN ACT RELATING TO LEGISLATIVE MEMBERS OF THE BOARD OF TRUSTEES OF THE UNIVERSITY OF VERMONT AND STATE AGRICULTURAL COLLEGE
    vt H.0566 AN ACT RELATING TO EXISTING AGRICULTURAL METHANE ELECTRIC GENERATION PLANTS
    vt H.0429 AN ACT RELATING TO A TUITION CREDIT FOR STUDENTS IN AGRICULTURAL PROGRAMS

Grab information about a specific bill:

    >>> bill = openstates.Bill.get('ca', '20092010', 'lower', 'AB20')
    >>> print bill.title
    An act to add Article 6 (commencing with Section 92060) to Chapter 1 of Part 57 of Division 9 of Title 3 of the Education Code, relating to the University of California.


List a bill's sponsors:

    >>> for sponsor in bill.sponsors:
    ...    print sponsor.name
    Solorio

List a bill's actions:

    >>> for action in bill.actions[0:3]:
    ...     print action
    lower (Desk): Read first time.  To print.
    lower (Desk): From printer.  May be heard in committee  January  1.
    lower (Committee CX09): Referred to Coms. on  HIGHER ED. and  B. & P.

View a bill's votes:

    >>> vote = bill.votes[0]
    >>> print vote.motion
    Do pass, but re-refer to the Committee on Banking, Finance and Insurance.
    >>> print vote.yes_count, vote.no_count, vote.other_count
    6 0 1

Lookup legislators by latitude and longitude:

    >>> legislators = openstates.Legislator.geo(35.79154, -78.7811169)
    >>> for l in legislators:
    ...     print l.full_name
    Nelson Dollar
    Josh Stein
