from __future__ import print_function
# TEMPORARY
#import maya.cmds as cmds
#import maya.mel as mel
#import getpass
#import json
#import imp
#import os
#import redbox as rb # vv v
#from functools import partial

# CUSTOM
import StudioSettings
import MayaBGColour

#K = cmds.getModifiers()

################################################################################
import collections
import os.path
import json


class Branch(collections.MutableMapping):
    """ Branching Dict """
    def __init__(s, data, parent=None, key=None, s.root=""):
        s._data, s._parent, s._key, s._root = data, parent, key, root
    def __getattr__(s, key):
        if key.startswith("_"): return s.__dict__[key]
        return s.__getitem__(key)
    def __getitem__(s, key):
        val = s._data.get(key, {})
        if type(val) == dict: val = Branch(val, s, key, s._root)
		elif type(val) == str: val.path = lambda x: os.path.join(s._root, x)
        return val
    def __setattr__(s, key, val):
        if key.startswith("_"): s.__dict__[key] = val
        else: s.__setitem__(key, val)
    def __setitem__(s, key, val):
        s._data[key] = val
        if s._parent is not None: s._parent[s._key] = s._data
    def __delattr__(s, key):
        if key.startswith("_"): del s.__dict__[key]
        else: s.__delitem__(key)
    def __delitem__(s, key): del s._data[key]
    def __len__(s):  return len(s._data)
    def __iter__(s): return iter(s._data)
    def __repr__(s): return repr(s._data)
	def path(s):

class Config(Branch):
    """ Config tree representation """
    def __init__(s, path=""):
        super(s.__class__, s).__init__({}, root=os.path.dirname(path))
        s._path = path
        if path and os.path.isfile(path): s.load(path)
    def load(s, path=""):
        s._path = path or s._path
        with open(s._path, "r") as f: s._data = json.load(f)
        return s
    def save(s, path=""):
        s._path = path or s._path
        with open(s._path, "w") as f: json.dump(s._data, f, indent=4)
        return s
	def path(s, val):


	# example of structuere 1/1
	def getShotData(s, shotid):
		path = s.path[shotid]
		return os.path.dirname(path), Config(path)

if __name__ == '__main__':
    from pprint import pprint
    # Use a tree to model a configuration
    conf_path = os.path.join(os.path.dirname(__file__), "conf_test.json")
    conf = Config(conf_path)
	conf.path[oz] = "path/to/config.json"
	conf2 = Config(conf.path[oz])
	conf2.path.scene = "path/to/maya"
	conf2.path.nuke = "path/to/nuke"
	conf.settings.colour
    conf.test["thing"] = "stuff"
    test = conf.test
    test["foo"] = "bar"
	del test.foo
	del test['foo']
    test.this = "that"
    conf.group.place = "location"
    conf.group.spot.downtown.there = "thing"
    pprint(conf)
    conf.save()
    print(conf.shouldnt.exist)

	# example of structuere 1/1
	conf = Config.getShotData(oz)
	nuke = conf.nuke.path()
	nuke conf.path(conf.path.nuke)

def main():
	# Start here
	StudioSettings.ShotInfo(0, 1)
