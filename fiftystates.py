import urllib, urllib2
import datetime
try:
    import json
except ImportError:
    import simplejson as json

class FiftyStatesApiError(Exception):
    pass
    
def apicall(func, params={}):
    params['format'] = 'json'
    url = 'http://174.129.25.59/api/%s/?%s' % (func,
                                              urllib.urlencode(params))
    try:
        response = urllib2.urlopen(url).read()
        obj = json.loads(response)
        return obj
    except urllib2.HTTPError, e:
        raise FiftyStatesApiError(e.read())
    except ValueError, e:
        raise FiftyStatesApiError('Invalid Response')

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

class FiftyStatesApiObject(object):
    
    def __init__(self, obj):
        self.__dict__.update(obj)
    
class Role(FiftyStatesApiObject):

    def __str__(self):
        return '%s %s %s district %s' % (self.state, self.chamber,
                                         self.session, self.district)
    
class Legislator(FiftyStatesApiObject):

    @staticmethod
    def get(id):
        func = 'legislator/%d' % id
        obj = apicall(func)
        return Legislator(obj)

    @staticmethod
    def search(**kwargs):
        func = 'legislator/search'
        obj = apicall(func, kwargs)
        return map(Legislator, obj)

    def __init__(self, obj):
        self.__dict__.update(obj)
        self.roles = map(Role, self.roles)

    def __str__(self):
        return self.full_name

class Vote(FiftyStatesApiObject):
    
    def __init__(self, obj):
        super(Vote, self).__init__(obj)
        self.date = parse_date(self.date)

    def __str__(self):
        return "Vote on '%s'" % self.motion

class Sponsor(FiftyStatesApiObject):
    
    def get_legislator(self):
        return Legislator.get(self.leg_id)

    def __str__(self):
        return self.full_name

class Action(FiftyStatesApiObject):
    
    def __init__(self, obj):
        super(Action, self).__init__(obj)
        self.date = parse_date(self.date)

    def __str__(self):
        return '%s: %s' % (self.actor, self.action)

class Session(FiftyStatesApiObject):

    def __str__(self):
        return self.name
    
class State(FiftyStatesApiObject):

    @staticmethod
    def get(abbrev):
        obj = apicall(abbrev)
        return State(obj)

    def __init__(self, obj):
        super(State, self).__init__(obj)
        self.sessions = map(Session, self.sessions)

    def __str__(self):
        return self.name

class Bill(FiftyStatesApiObject):

    @staticmethod
    def get(state, session, chamber, bill_id):
        func = '%s/bill/%s/%s/%s' % (state, session, chamber, bill_id)
        obj = apicall(func)
        return Bill(obj)

    def __init__(self, obj):
        super(Bill, self).__init__(obj)
        self.last_action = parse_date(self.last_action)
        self.date_added = parse_date(self.date_added)
        self.actions = map(Action, self.actions)
        self.sponsors = map(Sponsor, self.sponsors)
        self.votes = map(Vote, self.votes)

    def __str__(self):
        return '%s: %s' % (self.bill_id, self.title)
