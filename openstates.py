"""Python library for interacting with the Open State Project API.

The Open State Project provides data on state legislative activities,
including bill summaries, votes, sponsorships and state legislator
information.
"""
__author__ = "Michael Stephens <mstephens@sunlightfoundation.com>"
__copyright__ = "Copyright (c) 2010 Sunlight Labs"
__license__ = "BSD"
__version__ = "0.3.2"

from remoteobjects import RemoteObject, fields, ListObject
import urllib

OPENSTATES_URL = "http://openstates.sunlightlabs.com/api/v1/"

API_KEY = ''


class OpenStateDatetime(fields.Datetime):
    dateformat = '%Y-%m-%d %H:%M:%S'

    # None value for datetimes is fixed in trunk remoteobjects,
    # but broken on 1.1 release
    def decode(self, value):
        if value is None:
            return None
        return super(OpenStateDatetime, self).decode(value)


class OpenStateObject(RemoteObject):
    @classmethod
    def get(cls, func, params={}):
        params['format'] = 'json'
        params['apikey'] = API_KEY
        url = "%s%s/?%s" % (OPENSTATES_URL, func,
                            urllib.urlencode(params))
        return super(OpenStateObject, cls).get(url)


class Term(OpenStateObject):
    start_year = fields.Field()
    end_year = fields.Field()
    name = fields.Field()
    sessions = fields.List(fields.Field())

    def __str__(self):
        return self.name


class State(OpenStateObject):
    name = fields.Field()
    abbreviation = fields.Field()
    legislature_name = fields.Field()
    upper_chamber_name = fields.Field()
    lower_chamber_name = fields.Field()
    upper_chamber_term = fields.Field()
    lower_chamber_term = fields.Field()
    upper_chamber_title = fields.Field()
    lower_chamber_title = fields.Field()
    terms = fields.List(fields.Object(Term))

    @classmethod
    def get(cls, abbrev):
        """
        Get metadata about a state.

        :param abbrev: the state's two-letter abbreviation.
        """
        return super(State, cls).get('metadata/%s' % abbrev)

    def __str__(self):
        return self.name


class Action(OpenStateObject):
    date = OpenStateDatetime()
    actor = fields.Field()
    action = fields.Field()

    def __str__(self):
        return '%s: %s' % (self.actor, self.action)


class Sponsor(OpenStateObject):
    leg_id = fields.Field()
    name = fields.Field()
    type = fields.Field()
    chamber = fields.Field()

    def __str__(self):
        return self.full_name


class SpecificVote(OpenStateObject):
    leg_id = fields.Field()
    name = fields.Field()

    def __str__(self):
        return "%s <%s>" % (self.name, self.leg_id)


class Vote(OpenStateObject):
    date = OpenStateDatetime()
    chamber = fields.Field()
    committee = fields.Field()
    motion = fields.Field()
    yes_count = fields.Field()
    no_count = fields.Field()
    other_count = fields.Field()
    passed = fields.Field()
    type = fields.Field()
    yes_votes = fields.List(fields.Object(SpecificVote))
    no_votes = fields.List(fields.Object(SpecificVote))
    other_votes = fields.List(fields.Object(SpecificVote))

    def __str__(self):
        return "Vote on '%s'" % self.motion


class Version(OpenStateObject):
    url = fields.Field()
    name = fields.Field()


def ListOf(cls):
    class List(ListObject, OpenStateObject):
        entries = fields.List(fields.Object(cls))
    return List


class Bill(OpenStateObject):
    title = fields.Field()
    state = fields.Field()
    session = fields.Field()
    chamber = fields.Field()
    bill_id = fields.Field()
    actions = fields.List(fields.Object(Action))
    sponsors = fields.List(fields.Object(Sponsor))
    votes = fields.List(fields.Object(Vote))
    versions = fields.List(fields.Object(Version))
    alternate_titles = fields.List(fields.Field())

    @classmethod
    def get(cls, state, session, chamber, bill_id):
        """
        Get a specific bill.

        :param state: the two-letter abbreviation of the originating state
        :param session: the session identifier for the bill (see the state's
          metadata for legal values)
        :param chamber: which legislative chamber the bill originated in
          ('upper' or 'lower')
        :param bill_id: the bill's ID as assigned by the state
        """
        func = "bills/%s/%s/%s/%s" % (state, session, chamber, bill_id)
        return super(Bill, cls).get(func)

    @classmethod
    def search(cls, query, **kwargs):
        """
        Search bills.

        :param query: a query string which will be used to search bill titles

        Any additional keyword arguments will be used to further filter the
        results.
        """
        kwargs['q'] = query
        func = 'bills'
        return ListOf(cls).get(func, kwargs).entries

    def __str__(self):
        return '%s: %s' % (self.bill_id, self.title)


class Role(OpenStateObject):
    state = fields.Field()
    role = fields.Field()
    session = fields.Field()
    chamber = fields.Field()
    district = fields.Field()
    committee = fields.Field()
    contact_info = fields.List(fields.Dict(fields.Field()))
    start_date = OpenStateDatetime()
    end_date = OpenStateDatetime()
    party = fields.Field()

    def __str__(self):
        return '%s %s %s district %s' % (self.state, self.chamber,
                                         self.session, self.district)


class Legislator(OpenStateObject):
    leg_id = fields.Field()
    full_name = fields.Field()
    first_name = fields.Field()
    last_name = fields.Field()
    middle_name = fields.Field()
    suffix = fields.Field()
    party = fields.Field()
    roles = fields.List(fields.Object(Role))
    votesmart_id = fields.Field()

    @classmethod
    def get(cls, id):
        """
        Get a specific legislator.

        :param id: the legislator's Open State ID (e.g. 'TXL000139')
        """
        func = 'legislators/%s' % id
        return super(Legislator, cls).get(func)

    @classmethod
    def search(cls, **kwargs):
        """
        Search legislators.

        Use keyword arguments to filter by legislators fields.
        For example, `openstates.Legislator.search(last_name='Alesi')`.
        """
        return ListOf(cls).get('legislators', kwargs).entries

    @classmethod
    def geo(cls, lat, long):
        """
        Get all state legislators for a given lat/long pair

        :param lat: the latitude
        :param long: the longitude
        """
        func = 'legislators/geo'
        params = dict(lat=lat, long=long)
        return ListOf(cls).get(func, params).entries

    def __str__(self):
        return self.full_name


class CommitteeMember(OpenStateObject):
    leg_id = fields.Field()
    role = fields.Field()
    name = fields.Field('legislator')

class Committee(OpenStateObject):
    id = fields.Field()
    state = fields.Field()
    chamber = fields.Field()
    committee = fields.Field()
    subcommittee = fields.Field()
    members = fields.List(fields.Object(CommitteeMember))

    @classmethod
    def get(cls, id):
        """
        Get a committee.

        :param id: the committee's Open State ID (e.g. CAC000005)
        """
        func = 'committees/%s' % id
        return super(Committee, cls).get(func)

    @classmethod
    def search(cls, **kwargs):
        """
        Search comittees.

        Use keyword argmunents to filter by committee fields.
        For example, ``openstates.Committee.search(state='ca')``.
        """
        return ListOf(cls).get('committees', kwargs).entries
