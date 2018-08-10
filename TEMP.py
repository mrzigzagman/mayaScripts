
# TEMPORARY
print '# TEMP.py #'
import maya.cmds as cmds
#from functools import partial
#import colorsys
#import sys
#import maya.mel as mel
#import getpass
#import json
#import os
#import subprocess
#import os.path
#import imp
#import base64
#import collections
import sqlite3
import datetime
import time
import calendar
from datetime import date, timedelta

#import redbox as rb # vv v

# Jason's stuff
if 0:
    import sys; p="/weta/prod/motion/work/jdixon/python/"
    if p not in sys.path: sys.path.append(p)
    #import timetrack
    #import db


# CUSTOM
import StudioSettings
reload(StudioSettings)

import UIColourControl
reload(UIColourControl)

import UIWindowControl
reload(UIWindowControl)

K = cmds.getModifiers()

################################################################################

def main():
    import sys; p = "/vol/transfer/dyabu/Scripts/mayaScripts/"

    if p not in sys.path: sys.path.append(p)
    
    import TimeSheetDisplayTool
    reload(TimeSheetDisplayTool)
    TimeSheetDisplayTool.main()

    
    '''
    import colorsys

    a = [0.9, 0.9, 0.9]
    print a


    b = UIColourControl.RGBHSVconverter('ToHSV', a)
    print b

    c = UIColourControl.RGBHSVconverter('ToRGB', b)
    print c

    '''

