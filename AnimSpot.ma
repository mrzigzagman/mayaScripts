// Maya ASCII 2016ff07 scene
// Mane: AnimSpot.ma
// Codeset: UTF-8
requires maya "2016ff07";
createNode transform -n "StopWatch";
createNode locator -n "StopWatchShape" -p "StopWatch";
createNode animCurveTL -n "StopWatch_translateX";
    setAttr -s 7 ".ktv[0:6]" 1 0 5 0 7 0 9 0 11 0 15 0 30 0;
connectAttr "StopWatch_translateX.0" "StopWatch.tx"
// End of AnimSpot.ma
