#coding=utf-8

import json
import collections

class JSONSetEncoder(json.JSONEncoder):
  '''
  use json.dumps to allow sets to be encoded to json
  ref https://stackoverflow.com/questions/8230315/python-sets-are-not-json-serializable
  '''

  def default(self, o):
    if isinstance(o, collections.Set):
      return list(o)
    return super(JSONSetEncoder, self).default(o)


# or
'''
  File "/usr/lib64/python2.7/json/encoder.py", line 184, in default
    raise TypeError(repr(o) + " is not JSON serializable")
TypeError: datetime.datetime(2018, 11, 14, 2, 59, 49, 970355) is not JSON serializable
'''

class JSONDtmEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return '{}'.format(o)
        return super(JSONDtmEncoder, self).default(o)




def use():
  v = set()
  v1 = json.dumps(v,cls=JSONSetEncoder)
  
  v = {'timestamp': datetime.datetime.now()}
  v2 = json.dumps(v, cls=JSONDtmEncoder)
