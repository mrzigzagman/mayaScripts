
# TimeSheet Display Tool. 
# This builds a UI to visualize the hours worked.
# getting info from .db file.

import maya.cmds as cmds
from functools import partial
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

# CUSTOM
import StudioSettings
reload(StudioSettings)

import UIColourControl
reload(UIColourControl)

import UIWindowControl
reload(UIWindowControl)

#K = cmds.getModifiers()

################################################################################

K = cmds.getModifiers()

def main(): # UI BUILDER TEMPLATE 7.1.0
    global oUI
    oUI = UIWindowControl.UIBuilder()

    oUI.sUI = 'TimeSheet'
    oUI.Width = 900 # Total Width of Window in pixel (Default 320)
    oUI.Height = 600 # Total Height of Window in pixel
    oUI.iRowHeight = 25

    UIReBuild()

if __name__ == '__main__':
     main()

def UILayout():

    sColour = 'TimeSheet_WeekDay'
    oUI.iRowHeight = 25
    oUI.UIDivision([1,9,9,1,9,9,1,9,9,1,9,9,1,9,9,1,9,9,1,9,9,1], None, 25); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text('uiSun', l = ' ', h = oUI.iRowHeight, w = (oUI.Div[0][1]+oUI.Div[0][1]), bgc = UIColourControl.keywordColour('TimeSheet_WeekEnd')),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text('uiMon', l = ' ', h = oUI.iRowHeight, w = (oUI.Div[0][1]+oUI.Div[0][1]), bgc = UIColourControl.keywordColour(sColour)),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text('uiTue', l = ' ', h = oUI.iRowHeight, w = (oUI.Div[0][1]+oUI.Div[0][1]), bgc = UIColourControl.keywordColour(sColour)),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text('uiWed', l = ' ', h = oUI.iRowHeight, w = (oUI.Div[0][1]+oUI.Div[0][1]), bgc = UIColourControl.keywordColour(sColour)),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text('uiThu', l = ' ', h = oUI.iRowHeight, w = (oUI.Div[0][1]+oUI.Div[0][1]), bgc = UIColourControl.keywordColour(sColour)),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text('uiFri', l = ' ', h = oUI.iRowHeight, w = (oUI.Div[0][1]+oUI.Div[0][1]), bgc = UIColourControl.keywordColour(sColour)),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text('uiSat', l = ' ', h = oUI.iRowHeight, w = (oUI.Div[0][1]+oUI.Div[0][1]), bgc = UIColourControl.keywordColour('TimeSheet_WeekEnd')),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    ]; oUI.UIAddRow(aRow)

    #oUI.UIDivision([1], None, 0); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
    #cmds.separator( height = 5, style = 'none', w = oUI.Div[0][0] ),
    #]; oUI.UIAddRow(aRow)

    oUI.iRowHeight = 3
    # Row
    for i in range(0, 96):

        sColour = 'TimeSheet_Chart_OffWork_BG'
        if 36 < i <76: 
            sColour = 'TimeSheet_Chart_WorkHour_BG'

        for h in range(0, 98, 4):
            if i == h:
                sColour = 'TimeSheet_Chart_OffWork_Line'

        for h in range(36, 76, 4):
            if i == h:
                sColour = 'TimeSheet_Chart_WorkHour_Line'

        if i == 48:
            sColour = 'TimeSheet_Chart_Noon_Line'
        # Get time
        iMin = i * 15
        iH = iMin / 60
        iM = iMin % 60
        sTime = ('%s:%s'%(str(iH).zfill(2), str(iM).zfill(2)))
    

        oUI.UIDivision([1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1, 9,9,  1], None, 0); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0]),
        cmds.text('uiSun1_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.text('uiSun2_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][3], bgc = UIColourControl.keywordColour(sColour) ),
        cmds.text('uiMon1_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][4]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.text('uiMon2_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][5], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][6], bgc = UIColourControl.keywordColour(sColour) ),
        cmds.text('uiTue1_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][7]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.text('uiTue2_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][8], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][9], bgc = UIColourControl.keywordColour(sColour) ),
        cmds.text('uiWed1_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][10]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.text('uiWed2_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][11], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][12], bgc = UIColourControl.keywordColour(sColour) ),
        cmds.text('uiThu1_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][13]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.text('uiThu2_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][14], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][15], bgc = UIColourControl.keywordColour(sColour) ),
        cmds.text('uiFri1_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][16]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.text('uiFri2_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][17], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][18], bgc = UIColourControl.keywordColour(sColour) ),
        cmds.text('uiSat1_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][19]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.text('uiSat2_%s'%sTime, l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][20], bgc = UIColourControl.keywordColour(sColour)),
        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][21] ),
        ]; oUI.UIAddRow(aRow)
        #print 'uiSun1_%s'%sTime




    sColour = 'TimeSheet_TotalHours'
    oUI.iRowHeight = 20
    oUI.UIDivision([1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1, 9,9,  1], None, 0); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text(l = 'Total :', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
    cmds.text('uiSun2_Total', l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour(sColour)),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][3], bgc = UIColourControl.keywordColour(sColour) ),
    #cmds.text(l = 'Total :', h = oUI.iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour(sColour)),
    cmds.text('uiMon2_Total', l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][5]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][6], bgc = UIColourControl.keywordColour(sColour) ),
    #cmds.text(l = 'Total :', h = oUI.iRowHeight, w = oUI.Div[0][7], bgc = UIColourControl.keywordColour(sColour)),
    cmds.text('uiTue2_Total', l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][8]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][9], bgc = UIColourControl.keywordColour(sColour) ),
    #cmds.text(l = 'Total :', h = oUI.iRowHeight, w = oUI.Div[0][10], bgc = UIColourControl.keywordColour(sColour)),
    cmds.text('uiWed2_Total', l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][11]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][12], bgc = UIColourControl.keywordColour(sColour) ),
    #cmds.text(l = 'Total :', h = oUI.iRowHeight, w = oUI.Div[0][13], bgc = UIColourControl.keywordColour(sColour)),
    cmds.text('uiThu2_Total', l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][14]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][15], bgc = UIColourControl.keywordColour(sColour) ),
    #cmds.text(l = 'Total :', h = oUI.iRowHeight, w = oUI.Div[0][16], bgc = UIColourControl.keywordColour(sColour)),
    cmds.text('uiFri2_Total', l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][17]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][18], bgc = UIColourControl.keywordColour(sColour) ),
    #cmds.text(l = 'Total :', h = oUI.iRowHeight, w = oUI.Div[0][19], bgc = UIColourControl.keywordColour(sColour)),
    cmds.text('uiSat2_Total', l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][20]+oUI.Div[0][20], bgc = UIColourControl.keywordColour(sColour)),
    #cmds.text('uiSat3_Total', l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][20], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][21], bgc = UIColourControl.keywordColour(sColour) ),
    ]; oUI.UIAddRow(aRow)



    oUI.iRowHeight = 30
    sColour = 'TimeSheet_TotalHoursTS'
    oUI.UIDivision([1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1, 9,9,  1], None, 10); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text(l = 'From TS', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiSun2_TimeSheet', tx = ':00:00', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour), ec = partial(DayAdjust,'uiSun2_TimeSheet') ),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][3] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiMon2_TimeSheet', tx = ':00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour), ec = partial(DayAdjust,'uiMon2_TimeSheet'), tcc = partial(TextField_TimeCheck, 'uiMon2_TimeSheet') ),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][6] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][7], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiTue2_TimeSheet', tx = ':00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour), ec = partial(DayAdjust,'uiTue2_TimeSheet') ),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][9] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][10], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiWed2_TimeSheet', tx = ':00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour), ec = partial(DayAdjust,'uiWed2_TimeSheet') ),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][12] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][13], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiThu2_TimeSheet', tx = ':00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour), ec = partial(DayAdjust,'uiThu2_TimeSheet') ),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][15] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][16], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiFri2_TimeSheet', tx = ':00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour), ec = partial(DayAdjust,'uiFri2_TimeSheet') ),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][18] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][19], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiSat2_TimeSheet', tx = ':00:00', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour), ec = partial(DayAdjust,'uiSat2_TimeSheet') ),
    cmds.text('uiSat3_TimeSheet', l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][21] ),
    ]; oUI.UIAddRow(aRow) 


    oUI.iRowHeight = 10
    oUI.UIDivision([1], None, 0); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    ]; oUI.UIAddRow(aRow)  


    sColour = 'TimeSheet_Shade'
    oUI.iRowHeight = 20
    for i in range(len(aShotList)):
        oUI.UIDivision([1,  11,7,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1, 9,9,  1], None, 0); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
        cmds.text('uiSun1_shot%s'%i, l = aShotList[i][12:].replace('/', ' '), h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.textField('uiSun2_shot%s'%i, tx = '', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour(sColour)),
        cmds.button('uiSun2_shot%s'%i, label = '', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
        #cmds.text('uiMon1_shot%s'%i, l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.textField('uiMon2_shot%s'%i, tx = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        cmds.button('uiMon2_shot%s'%i, label = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
        #cmds.text('uiTue1_shot%s'%i, l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.textField('uiTue2_shot%s'%i, tx = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        cmds.button('uiTue2_shot%s'%i, label = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
        #cmds.text('uiWed1_shot%s'%i, l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.textField('uiWed2_shot%s'%i, tx = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        cmds.button('uiWed2_shot%s'%i, label = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
        #cmds.text('uiThu1_shot%s'%i, l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.textField('uiThu2_shot%s'%i, tx = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        cmds.button('uiThu2_shot%s'%i, label = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
        #cmds.text('uiFri1_shot%s'%i, l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.textField('uiFri2_shot%s'%i, tx = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        cmds.button('uiFri2_shot%s'%i, label = '', h = oUI.iRowHeight, w = oUI.Div[0][2]+oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
        #cmds.text('uiSat1_shot%s'%i, l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour)),
        #cmds.textField('uiSat2_shot%s'%i, tx = '', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour(sColour)),
        cmds.button('uiSat2_shot%s'%i, label = '', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour(sColour)),

        cmds.textField('uiSat3_shot%s'%i, tx = '', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour('MayaBG')),

        cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][21] ),
        ]; oUI.UIAddRow(aRow)

    '''
    oUI.UIDivision([1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1,  9,9,  1, 9,9,  1], None, 10); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][0] ),
    cmds.text(l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiSun2_Temp', tx = '00:00', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][3] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiMon2_Temp', tx = '00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][6] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][7], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiTue2_Temp', tx = '00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][9] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][10], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiWed2_Temp', tx = '00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][12] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][13], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiThu2_Temp', tx = '00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][15] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][16], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiFri2_Temp', tx = '00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),

    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][18] ),
    #cmds.text(l = ' ', h = oUI.iRowHeight, w = oUI.Div[0][19], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.textField('uiSat2_Temp', tx = '00:00', h = oUI.iRowHeight, w = oUI.Div[0][1]+oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.text('uiSat3_Temp', l = '', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('MayaBG')),
    cmds.separator( height = oUI.iRowHeight, style = 'none', w = oUI.Div[0][21] ),
    ]; oUI.UIAddRow(aRow) 

    '''
    '''
    # Row
    oUI.UIDivision([.6,.6,.6,1,1.8,.7,0.1,1], None, 0); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
    cmds.text(l = 'Range :', h = oUI.iRowHeight, w = oUI.Div[0][0]),
    cmds.textField(tx = '1001', h = oUI.iRowHeight, w = oUI.Div[0][1]),
    cmds.textField(tx = '1216', h = oUI.iRowHeight, w = oUI.Div[0][2]),
    cmds.button(label = 'Current range', h = oUI.iRowHeight, w = oUI.Div[0][3], bgc = UIColourControl.keywordColour('Tone2'), enableBackground = False),
    cmds.button(label = 'PlayBlast            [1]', h = oUI.iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour('Tone2'), enableBackground = False),
    cmds.button(label = '[2]', h = oUI.iRowHeight, w = oUI.Div[0][5], bgc = (0, .1, .1), enableBackground = False),
    cmds.button(label = '', h = oUI.iRowHeight, w = oUI.Div[0][6]),
    cmds.button(label = 'Current', h = oUI.iRowHeight, w = oUI.Div[0][7], bgc = (0, .1, .1), enableBackground = False),
    ]; oUI.UIAddRow(aRow)


    ## Row
    oUI.UIDivision([.6,.6,.6,1,1.1,0.7,0.7,0.1,1]); aRow = [
    cmds.text(l = 'Set : ', h = oUI.iRowHeight, w = oUI.Div[0][0]),
    cmds.button(label = 'Bigger', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = (1,1,1), enableBackground = False, c = partial(UIButton_Bigger, 500) ),
    cmds.button(label = 'Smaller', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = (1,1,1), enableBackground = False, c = partial(UIButton_Smaller, 100) ),
    cmds.button(label = 'Prod Range', h = oUI.iRowHeight, w = oUI.Div[0][3], bgc = (1,1,1), enableBackground = False),
    cmds.text(l = '', h = oUI.iRowHeight, w = oUI.Div[0][4]),
    cmds.button(label = '[3]', h = oUI.iRowHeight, w = oUI.Div[0][5], bgc = (1,1,1), enableBackground = False),
    cmds.separator(height = 40, style = 'in', w = oUI.Div[0][6]),
    cmds.separator(height = 40, style = 'in', w = oUI.Div[0][7]),
    cmds.button(label = 'Marked', h = oUI.iRowHeight, w = oUI.Div[0][8], bgc = (1,1,1), enableBackground = False),
    ]; oUI.UIAddRow(aRow)


    ## Row
    oUI.UIDivision([.6,1.2,1,0.4,.7,1.4,0.1,1]); aRow = [
    cmds.text(l = 'Weta : ', h = oUI.iRowHeight, w = oUI.Div[0][0]),
    cmds.button(label = 'BLAST', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = (0,.1,.1), enableBackground = False),
    cmds.button(label = 'SHOTSUB', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = (0,.1,.1), enableBackground = False),
    cmds.text(l = '', h = oUI.iRowHeight, w = oUI.Div[0][3]),
    cmds.button(label = 'Saved', h = oUI.iRowHeight, w = oUI.Div[0][4], bgc = (0,.1,.1), enableBackground = False ),
    AddDropMenu('DropdownMenu', oUI.Div[0][5], 4, 'drop', Dropdown_Changed, ['test1','test2','test3','test4'], 1),
    cmds.text(l = '', h = oUI.iRowHeight, w = oUI.Div[0][6]),
    cmds.button(label = 'Range', h = oUI.iRowHeight, w = oUI.Div[0][7], bgc = (0,.1,.1), enableBackground = False ),
    ]; oUI.UIAddRow(aRow)

    ## Row
    oUI.UIDivision([1,1]); aRow = [
    cmds.floatSliderGrp('floatSlider1', label = 'Size', field = True, h = oUI.iRowHeight, w = oUI.Div[0][0], cw = [1, 25], cc = partial(FloatSlider_Changed, 'floatSlider1'), minValue = 0.1, maxValue = 2.0, fieldMinValue = 0.1, fieldMaxValue = 2.0, value = 1),
    cmds.floatSliderGrp('floatSlider2', label = 'Size', field = True, h = oUI.iRowHeight, w = oUI.Div[0][0], cw = [1,25], cc = partial(FloatSlider_Changed, 'floatSlider2'), minValue = 0.1, maxValue = 2.0, fieldMinValue = 0.1, fieldMaxValue = 2.0, value = 1),
    ]; oUI.UIAddRow(aRow)

    ## Row
    oUI.UIDivision([1,1,1,1,1]); aRow = [
    cmds.separator( height = 40, style = 'none', w = oUI.Div[0][0] ),
    cmds.separator( height = 40, style = 'single', w = oUI.Div[0][0] ),
    cmds.separator( height = 40, style = 'out', w = oUI.Div[0][0] ),
    cmds.separator( height = 40, style = 'in', w = oUI.Div[0][0] ),
    cmds.separator( height = 40, style = 'shelf', w = oUI.Div[0][0] ),
    ]; oUI.UIAddRow(aRow)

    ## Row
    oUI.UIDivision([1]); aRow = [
    cmds.textField('uiTextField', w = oUI.Div[0][0], bgc = UIColourControl.keywordColour('Tone1'), tcc = partial(TextField_TextCheck, 'uiTextField'), cc = partial(TextField_TextShow, 'uiTextField')),
    ]; oUI.UIAddRow(aRow)
    '''
def convertMin(oValue): 
    # if oValue is int:
    if isinstance(oValue, int):
        return '%s:%s'%(str(oValue/60), str(oValue%60).zfill(2))
    else:
        return int(oValue.split(':')[0]) * 60 + int(oValue.split(':')[1])
        


def DayAdjust(sUITimeSheet, *args):
    aWeekInfo = getWeeklyTimeInfo()
    aShotList = []
    for a in aWeekInfo:
        for s in a[1]:
            if not s[0] in aShotList:
                aShotList.append(s[0])

    sTotal = cmds.text(sUITimeSheet.replace('TimeSheet', 'Total'), q = True, l = True)
    sTimeSheet = cmds.textField(sUITimeSheet, q = True, tx = True)

    iTotalMin = convertMin(sTotal)
    iTotalTimeSheet = convertMin(sTimeSheet)
    #tDifference = timedelta(hours=int(sTotal.split(':')[0]), minutes=int(sTotal.split(':')[1])) - timedelta(hours=int(sTimeSheet.split(':')[0]), minutes=int(sTimeSheet.split(':')[1]))
    iDifference = iTotalMin - iTotalTimeSheet
    #print 
    #print 'iTotalMin       ', convertMin(iTotalMin)
    #print 'iTotalTimeSheet ', convertMin(iTotalTimeSheet)
    #print 'iDifference     ', convertMin(iDifference), iDifference


    # Re Calculate Total week hour
    iWeek = 0
    aWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for s in aWeek:
        sWeek = cmds.textField('ui%s2_TimeSheet'%s, q = True, tx = True)
        iWeek += convertMin(sWeek) 
    
    sWeek = convertMin(iWeek) 

    cmds.text('uiSat3_TimeSheet', e = True, l = sWeek)



    # Add total work hour from all shots for this day. (get in aHour )
    aHour = []
    for w in aWeek:
        for i in range(len(aShotList)):
            iHour = 0
            sShot = 'ui%s2_shot%s'%(w, i)
            #sHour = cmds.textField(sShot, q = True, tx = True)
            sHour = cmds.button(sShot, q = True, label = True)
            if sHour:
                #print sHour.split(':')
                iHour += convertMin(sHour)
                #print iHour 

            if sShot.split('_')[0] == sUITimeSheet.split('_')[0]:
                aHour.append(iHour)


    #print 'aHour', convertMin(sum(aHour)), aHour
    iEmergency = 0
    # Logic to split the differences
    if iDifference == iTotalMin:
        aHour = [0 for i in aHour]
    elif iDifference < 0: # if the hour compensation needs adding to the logged hours.
        # Loop through aHour to add 15 min (for adjustment that more than enough to add all entries.)
        iLoop = (abs(iDifference) / 15) / sum([1 for x in aHour if x])
        #print 'iLoop', iLoop
        for i in range(iLoop):
            if aHour[i]:
                aHour[i] += 15

        # Loop through to add 15. For the remainders left (This will not loop once completely.)
        iRemain = (abs(iDifference) / 15) % sum([1 for x in aHour if x])
        aOrder = aHour[:]
        aOrder.sort(reverse = True)
        #print 'aOrder', aOrder
        for h in aOrder:
            if iRemain:
                aHour[aHour.index(h)] += 15
                iRemain -= 1

    elif iDifference > 0: # if subtracting from the logged hours.
        iUnder60 = 0
        aSkipped = [0] * len(aHour)
        iEmergency = 0
        while iDifference > 0:
            for i, h in enumerate(aHour[:]):
                a60Plus = [x for x, e in enumerate(aHour) if e > 60]
                #print 'a60Plus', a60Plus
                if a60Plus:
                    for x in a60Plus[:]:
                        if iDifference:
                            aHour[x] -= 15
                            iDifference -=15

                else:
                    a15Plus = [x for x, e in enumerate(aHour) if e > 15]
                    for x in a15Plus:
                        if iDifference:
                            aHour[x] -= 15
                            iDifference -=15
                    
            iEmergency += 1
            if iEmergency > 50:
                iDifference = 0

    #print 'iEmergency', iEmergency
    #print 'aHour', convertMin(sum(aHour)), aHour


    # Re-Write to textFields
    sWeek = sUITimeSheet[:6]
    for i, h in enumerate(aHour):
        if h <= 0:
            cmds.button('%s_shot%s'%(sWeek, i), e = True, label = '') 
        elif h:
            #print '%s_Shot%s'%(sWeek, i)
            #cmds.textField('%s_shot%s'%(sWeek, i), e = True, tx = '%s:%s'%(str(h/60).zfill(2), str(h%60).zfill(2)))
            cmds.button('%s_shot%s'%(sWeek, i), e = True, label = convertMin(h))

    sTotal = cmds.text(sUITimeSheet.replace('TimeSheet', 'Total'), e = True, l = convertMin(sum(aHour)))



def UIReBuild():
    global oUI, iShotsLength, aShotList


    aWeekInfo = getWeeklyTimeInfo()
    aShotList = []
    iShotsLength = 0
    for a in aWeekInfo:
        for s in a[1]:
            if not s[0] in aShotList:
                aShotList.append(s[0])
    aShotList.sort()                
    oUI.UIPrepare()
    UILayout()
    oUI.UICreate()

    aUIWEEK = ['uiSun', 'uiMon', 'uiTue','uiWed','uiThu','uiFri','uiSat']

    # Colour Assignment to each shot:
    rgbKeyColour = UIColourControl.keywordColour('TimeSheetChartColour')
    aUICOLOUR = [] 

    #RGBHSVconverter(sType = 'ToRGB', aColour = [1, 1, 1]):
    #def convertRGBvaluesToScaleOf(iType = 1, aRGB = []): # iType is 1 or 255
    #def offsetRGBvalues(aRGB = [0.0, 0.0, 0.0], R = 0.0, G = 0.0, B = 0.0):
    iIncrement = -0.8 / float(len(aShotList)-1)

    if iIncrement < -0.2:
        iIncrement = -0.2
    #iIncrement = -0.1
    sShotNumber = aShotList[0].split('/')[-2]
    iHue = 0
    #print 'rgbKeyColour ', rgbKeyColour
    for i, a in enumerate(aShotList):
        #print a
        oColour = UIColourControl.offsetRGBvalues(rgbKeyColour, i * iIncrement, i * iIncrement, i * iIncrement)
        


        if not aShotList[i].split('/')[-2] == sShotNumber:
            #print '    ', sShotNumber
            sShotNumber = aShotList[i].split('/')[-2]
            iHue += 0.05

        #print 
        #print 'rgb Colour Before', oColour
        hsvColour = UIColourControl.RGBHSVconverter('ToHSV', oColour)
        #print 'hsvColour        ', hsvColour
        hsvColour[0] = hsvColour[0] + iHue
        #print 'hsvColour with Hue', hsvColour
        rgbColour = UIColourControl.RGBHSVconverter('toRGB', hsvColour)
        #print 'rgb Colour After ', rgbColour        



        aUICOLOUR.append(rgbColour)



    for w, a in enumerate(aWeekInfo):
        #print 
        #print a[0]
        #print a[0]
        cmds.text(aUIWEEK[w], e = True, l = a[0])
        atShotHours = []
        tTotalTime = timedelta(hours=0, minutes=0)

        for b in a[1]:
            #print '     ',b[0]
            oColour = aUICOLOUR[aShotList.index(b[0])]
            #print oColour
            atShotHours.append(None)
            tDif = timedelta(hours=0, minutes=0)
            for c in b[1]:
                iTimeCheck = 1
                aStart = c[0].split(':')

                while iTimeCheck:
                    if ':'.join(aStart) == c[1]:
                        iTimeCheck = 0
                    cmds.text('%s1_%s'%(aUIWEEK[w], ':'.join(aStart)), e = True, l = ' ', bgc = oColour),
                    if aStart[1] == '45':
                        aStart[1] = '00'
                        aStart[0] = str(int(aStart[0]) + 1).zfill(2)
                    else:
                        aStart[1] = str(int(aStart[1]) + 15)

                # adding up time worked
                tStart = c[0].split(':')
                tEnd = c[1].split(':')


                tTemp = timedelta(hours=int(tEnd[0]), minutes=int(tEnd[1])) - timedelta(hours=int(tStart[0]), minutes=int(tStart[1])) + timedelta(hours=0, minutes=15)
                tDif += tTemp
                #print '       ', c, tTemp
                atShotHours.append(tDif)


            cmds.text('uiSun1_shot%s'%(aShotList.index(b[0]) ) , e = True, bgc = oColour)
            #cmds.textField('%s2_shot%s'%(aUIWEEK[w], aShotList.index(b[0]) ) , e = True, tx = str(atShotHours[-1])[:-3], bgc = oColour)
            cmds.button('%s2_shot%s'%(aUIWEEK[w], aShotList.index(b[0]) ) , e = True, label = str(atShotHours[-1])[:-3], bgc = oColour)
            #print 'Total Shot Time : ', atShotHours[-1]
            tTotalTime += atShotHours[-1]
            

        cmds.text('%s2_Total'%(aUIWEEK[w] ), e = True, l = str(tTotalTime)[:-3])
        cmds.textField('%s2_TimeSheet'%(aUIWEEK[w] ), e = True, tx = str(tTotalTime)[:-3])



    # Re Calculate Total week hour
    iWeek = 0
    aWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for s in aWeek:
        
        sWeek = cmds.textField('ui%s2_TimeSheet'%s, q = True, tx = True)
        iWeek += int(str(sWeek).split(':')[0]) * 60 + int(str(sWeek).split(':')[1])
    
    sWeek = '%s:%s'%(str(iWeek/60).zfill(2), str(iWeek%60).zfill(2))

    cmds.text('uiSat3_TimeSheet', e = True, l = sWeek)

    # Add total work hour from all shots

    for w in aWeek:
        iHour = 0
        for i in range(len(aShotList)):
            #sHour = cmds.textField('ui%s2_shot%s'%(w, i), q = True, tx = True)
            sHour = cmds.button('ui%s2_shot%s'%(w, i), q = True, label = True)
            if sHour:
                #print sHour.split(':')
                iHour += int(sHour.split(':')[0]) *60 + int(sHour.split(':')[1])
                #print iHour 

        #cmds.textField('ui%s2_Temp'%w, e = True, tx = '%s:%s'%(str(iHour/60).zfill(2), str(iHour%60).zfill(2)))
            


def TextField_TextCheck(sFieldName, *args):
    oUI.StringCheck_FileName(sFieldName)

def TextField_TimeCheck(sFieldName, *args):
    oUI.StringCheck_Hours(sFieldName)

def TextField_TextShow(sFieldName, *args):
    sText = cmds.textField(sFieldName, tx = True, q = True)

    aPrint = UIColourControl.inViewMessageColourPreset('Red', sText)
    cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def UIButton_Bigger(iHeight, *args):
    oUI.Height = iHeight
    UIReBuild()

    aPrint = UIColourControl.inViewMessageColourPreset('Red', 'BIGGER!!')
    cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def UIButton_Smaller(iHeight, *args):
    oUI.Height = iHeight
    UIReBuild()


    aPrint = UIColourControl.inViewMessageColourPreset('Blue', 'SMALLER!!')
    cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )


def FloatSlider_Changed(sGrp, *args):
    print 'Float Slider Changed %s'% sGrp
    print cmds.floatSliderGrp(sGrp, q = True, v = True)

    if sGrp.endswith('1'):
        cmds.floatSliderGrp(sGrp, e = True, v = 1)





def Dropdown_Changed(*args):
    print cmds.optionMenu('DropdownMenu', q = True, value = True)


### UI CREATION FUNCTIONS ###
def AddDropMenu(sName, fWidth, iLen, sLabel, CC, aList, iMenu):
    '''
    A custom function to add optionMenu(...) to UIAddRow() WITH menus already attached.

    AddDropMenu(sName, FWidth, iLen, sLabel, CC, aList, iMenu)
    sName : Unique ID Name to refer back to edit later.
    fWidth : Width of the menu item
    iLen : The number of selectable menus. (To be used as : if only one: gray out and lock it.)
    sLabel : label of the menu = '' nothing. don't need in this case.
    CC: Change Command : to run when menu is changed.
    aList : list of menus to display

    iMenu : to be used as index of aDropMenu to store what's listing currently. (Later to be deleted all and re-created at change command)
    '''

    iMenu -= 1 # Be used as index of aDropMenu

    # Set the dropmenu to gray if there is only one menu. (no need to change anyways.)
    if iLen == 1:
        iLen = False
    else:
        iLen = True

    oCMD = cmds.optionMenu(sName, label = sLabel, en = iLen, w = fWidth, cc = CC)

    # Add selectable menus to above optionMenu.
    for l in aList:
        cmds.menuItem(l, label = l)
        #aDropMenu[iMenu].append(l)

    return oCMD



def getWeeklyTimeInfo():
    iWeekAgo = 1

    ### TIME STUFF ###
    oToday = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    iWeekday = oToday.weekday() +1
    if iWeekday == 7 : iWeekday = 0

    aWeek = [calendar.day_name[i] for i in [6, 0, 1, 2, 3, 4, 5] ]
    oSunday = oToday - timedelta(iWeekday) - timedelta(weeks = iWeekAgo) # Get Sunday of the week. (Start of the week)
    aWeekRange = [[oSunday + timedelta(days = w), oSunday + timedelta(days = w) + timedelta(days = 1) - timedelta(seconds=1)] for w in range(0, 7)]


    sPath = '/usr/home/dyabu/timesheet.db'
    sTable = 'timesheet'

    conn = sqlite3.connect(sPath)
    c = conn.cursor()

    aWeekInfo = [] # The main array contain all info to output

    for wr in aWeekRange:
        st = time.mktime(wr[0].timetuple())
        ed = time.mktime(wr[1].timetuple())

        aWeekInfo.append([str(wr[0])[:10], st, ed]) # at the top, store the date


    for v, w in enumerate(aWeekInfo[:]):

        # separate to daily
        c.execute('SELECT * FROM {tn} WHERE checkin BETWEEN {sr} AND {ed}'.format(tn = sTable, sr = w[1], ed = w[2]))
        aRowsForOneDay = c.fetchall()

        aShot = []
        aList = []
        for d in aRowsForOneDay:
            if not d[8] in aList:
                aShot.append([d[8], []])
                aList.append(d[8])
        #print aList
        for d in aRowsForOneDay:
            for i, s in enumerate(aShot[:]):
                if d[8] == s[0]:
                    aShot[i][1].append(d[1])

        #print v
        aWeekInfo[v].append(aShot)

    # Cleanup and Re-Organize aWeekInfo
    aTemp = aWeekInfo
    aWeekInfo = []
    for i, a in enumerate(aTemp[:]):
        aWeekInfo.append([a[0], []])

        for x, b in enumerate(a[3]):
            aWeekInfo[i][1].append([b[0], []])

            iBefore = 0.0
            aTimeRange = []
            iStart = None
            iEnd = None

            for v, c in enumerate(b[1][:]):

                if not iStart:
                    iStart = c
                    iBefore = c
                    iEnd = None

                iAfter = c
                if int(iAfter) == int(iBefore):
                    pass
                elif (iAfter - iBefore) <= 900:
                    iBefore = iAfter
                else:
                    iEnd = iBefore + 300

                if v == len(b[1])-1:
                    if not iEnd:
                        iEnd = iAfter + 300

                if iEnd:
                    aRecord = [datetime.datetime.fromtimestamp(iStart).strftime('%H:%M'), datetime.datetime.fromtimestamp(iEnd).strftime('%H:%M')]
                    for e, t in enumerate(aRecord[:]): # This loop sets time in 15min increment. 
                        aMin = t.split(':')
                        iMin = int(aMin[1])
                        if 8 <= iMin <= 22:
                            aMin[1] = '15'
                        elif 23 <= iMin <= 38:
                            aMin[1] = '30'
                        elif 37 <= iMin <= 52:
                            aMin[1] = '45'
                        elif 0 <= iMin <= 7:
                            aMin[1] = '00'
                        else:                     
                            aMin[1] = '00'
                            aMin[0] = '%s'%str(int(aMin[0])+1).zfill(2)
                        
                        aRecord[e] = ':'.join(aMin)
         
                    aTimeRange.append(aRecord)
                    iStart = c
                    iEnd = None
                    iBefore = iAfter

            aWeekInfo[i][1][x][1] = aTimeRange
    
    
    if 0: # print the content of aWeekInfo
        print '###################'
        for a in aWeekInfo:
            print a[0]

            for b in a[1]:
                print '     ', b[0]
                for c in b[1]:
                    print '          ',c

    return aWeekInfo

