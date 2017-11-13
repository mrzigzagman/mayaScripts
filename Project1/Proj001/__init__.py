import os
import re
import os.path
import utility
import subprocess
from enum import Enum
import mo.wm.tools.fileBrowser as fileBrowser
from mo.wt.libs.imageSequence import Seq
from mo.wm.libs.openMaya import displayErrorOnFail

import maya.cmds as cmds


ROOT = os.path.dirname(__file__)
CONVERT_TOOL_PATH = os.path.join(ROOT, 'nuke_convert.py')

VERSION = '1'

COLOUR = [
    (0.4, 0.2, 0.2), # Red
    (0.2, 0.4, 0.2), # G
    (0.8, 0.1, 0.1), # R
    (0.5, 0.5, 0.0),] # Y

PROJECT_ROOT = os.path.join(
    '/',
    'proj',
    os.environ['FILM'],
    os.environ['TREE'],
    os.environ['SCENE'],
    os.environ['SHOT'])

Class Widget(object):
    '''
    Wrapper for widgets.
    '''
    def  __init__(s, func, *args, **kwargs):
        s.func = func
        s.widget = func(*args, **kwargs)
    def query(s, tag):
        return s.func(s.widget, **{'q': True, tag:True})
    def edit(s, **kwargs):
        kwargs['e'] = True
        s.func(s.widget, **kwargs)
        return s
    def enable(s):
        return s.edit(en = True)
    def disable(s):
        return s.edit(en = False)





class Main(object):
    '''
