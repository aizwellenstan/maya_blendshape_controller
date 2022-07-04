import maya.cmds as cmds
import maya.OpenMaya as om
global bspTsl
global bspWeightTsl

def bspConnectToolUI():
    global bspTsl
    global bspWeightTsl
    bspConnectWin = 'コネクションツール'
    if cmds.window(bspConnectWin, exists=True):
        cmds.deleteUI(bspConnectWin)
    bspConnectWin = cmds.window('コネクションツール', sizeable=True)
    rc = cmds.rowColumnLayout(numberOfColumns=1)
    cmds.separator(style = 'in')
    cmds.text(label = 'Select object and click the button below', height=30)
    cmds.separator(style = 'in')
    cmds.button(label = 'Load BlendShapes', height=30, command='loadBsp()', backgroundColor=[.7,1,0])
    cmds.separator(style = 'in')
    loadBsptsl = cmds.textScrollList(allowMultiSelection = False, height=50, selectCommand='loadBspWeight()')
    bspTsl = loadBsptsl
    cmds.separator(style = 'in')
    cmds.text(label='list of selective weights', height=30)
    cmds.separator(style = 'in')
    tScrollList = cmds.textScrollList(allowMultiSelection=True, height=160)
    bspWeightTsl = tScrollList
    cmds.separator(style = 'in')
    cmds.button(label = 'Add Attributes and Connect BlendShape', height=30, command='connections()', backgroundColor=[.7,1,0])
    cmds.separator(style = 'in')
    cmds.separator(style = 'double')
    cmds.text(label = '---BlendShape Connect Tool---', height=20, font='boldLabelFont')
    cmds.text('Script By: github.com/aizwellentan aizwellenstan@gmail.com')
    cmds.text(label = '', height=5)
    cmds.separator(style = 'double')
    cmds.separator(style = 'in')
    cmds.button(label = 'Refresh Window', height=30, command='bspConnectToolUI()', backgroundColor=[1,.2,0])
    cmds.separator(style = 'in')
    cmds.showWindow(bspConnectWin)
    om.MGlobal.displayInfo('---BlendShape Connect Tool---')

def loadBsp():
    listSelection = cmds.ls(selection=True)
    if listSelection == []:
        om.MGlobal.displayWarring('select object first then click the button')
    else:
        shapeNode = cmds.listRelatives(listSelection[0], children=True)
        findSet = cmds.listConnections(shapeNode[0], source=False, destination=True)
        cmds.textScrollList(bspTsl, edit=True, removeAll=True)
        blendShapes = []
        for i in findSet:
            bspNode = cmds.listConnections(i, source=True, destination=False, type='blendShape')
            if not bspNode == None:
                blendShapes.append(bspNode[0])
        cmds.textScrollList(bspTsl, edit=True, append=blendShapes)
        om.MGlobal.displayInfo('BlendShapes Loaded')
    
def loadBspWeight():
    qloadBsptsl = cmds.textScrollList(bspTsl, query=True, selectItem=True)
    cmds.textScrollList(bspWeightTsl, edit=True, removeAll=True)
    for i in qloadBsptsl:
        bspAttr = cmds.listAttr(i + '.weight', multi=True)
        cmds.textScrollList(bspWeightTsl, edit=True, append=bspAttr)
    om.MGlobal.displayInfo('Blendshapes Weights loaded')

def connections():
    qSelectedItem = cmds.textScrollList(bspWeightTsl, query = True, selectItem=True)
    qbspNode = cmds.textScrollList(bspTsl, query=True, selectItem=True)
    ctrlSelection = cmds.ls(selection=True)
    for i in qSelectedItem:
        cmds.addAttr(longName=i, attributeType='float', minValue=0, maxValue=1, defaultValue=0, keyable=True)
        cmds.connectAttr(ctrlSelection[0] + '.' + i, qbspNode[0] + '.' + i, force=True)
    om.MGlobal.displayInfo('blendShapes Connected')

bspConnectToolUI()
