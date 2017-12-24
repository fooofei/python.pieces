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





def use():
  v = set()
  v1 = json.dumps(v,cls=JSONSetEncoder)
