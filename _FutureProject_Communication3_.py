from __future__ import print_function # From python 3

import collections
import os.path
import json

class Branch(collections.MutableMapping):
    """ Branching Dict """
    def __init__(s, data, parent=None, key=None, getfilter=(lambda val: val), setfilter=(lambda key,val: val)):
        s._data, s._parent, s._key, s._getfilter, s._setfilter = data, parent, key, getfilter, setfilter
    def __getattr__(s, key):
        if key.startswith("_"): return s.__dict__[key]
        return s.__getitem__(key)
    def __getitem__(s, key):
        val = s._data.get(key, {})
        val_type = type(val)
        if val_type == dict: val = Branch(val, parent=s, key=key, getfilter=s._getfilter, setfilter=s._setfilter)
        return s._getfilter(val)
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
    def __call__(s, val): # Transform values
        if s._parent is None: raise TypeError("Root is not callable.")
        s._parent[s._key] = s._setfilter(s._key, val)

class Config(Branch):
    """ Config tree representation """
    def __init__(s, path=""):
        super(s.__class__, s).__init__({}, setfilter=s.setfilter, getfilter=s.getfilter)
        s._path = path
        s._root = os.path.dirname(path)
        if path and os.path.isfile(path): s.load(path)
    def load(s, path=""):
        s._path = path or s._path
        s._root = os.path.dirname(s._path)
        with open(s._path, "r") as f: s._data = json.load(f)
        return s
    def save(s, path=""):
        s._path = path or s._path
        s._root = os.path.dirname(s._path)
        with open(s._path, "w") as f: json.dump(s._data, f, indent=4)
        return s
    def setfilter(s, key, val):
        if key == "path" and (type(val) == str or type(val) == unicode):
            val = "PATH:" + os.path.relpath(val, s._root)
        elif key == "conf" and (type(val) == str or type(val) == unicode):
            val = "CONF:" + os.path.relpath(val, s._root)
        return val
    def getfilter(val):
        if (type(val) == str or type(val) == unicode) and val.startswith("PATH:"):
            val = os.path.join(s._root, val)
        elif (type(val) == str or type(val) == unicode) and val.startswith("CONF:"):
            val = Config(os.path.join(s._root, val))
        return val

if __name__ == '__main__':
    from pprint import pprint
    # Example
    root = os.path.dirname(__file__)
    conf = Config(os.path.join(root, "conf.json"))
    conf.nuke.source.path(os.path.join(root, "nukefile.nk")) # { "nuke": { "source": "PATH:nukefile.nk" } }
    print(conf.nuke.source) # "/long/path/to/nukefile.nk"
    conf.nuke.tracking = "thing" # { "nuke" : {"tracking" : "thing"} }
    print(conf.nuke.tracking) # "thing"
    conf.save()

    conf2 = Config(os.path.join(sPathNewLocatoin, "conf2.json"))
    conf2.maya.source.path("path/to/source")
    conf2.save()
    conf.scenes.oz.conf(os.path.join(sPathNewLocatoin, "conf2.json")) # { "scenes" : { "oz" : "CONF:path/to/conf2.json"} }

    # -------- Undertoood --------

    # To be continued HERE!!!!
    print(conf.scenes.oz) # Config() == conf2
    print(conf.scenes.oz.maya.source) # Magic happens here!!
