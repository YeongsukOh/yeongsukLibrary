import maya.cmds as cmds

def setList():
    selectionList = cmds.ls(sl = True)
    if len(selectionList) > 0:
        if len(selectionList) % 2 == 0:
            number = int(len(selectionList)/2)
            driver = selectionList[:number]
            driven = selectionList[number:]
            return number, driver, driven
        else:
            raise Exception("select one more items")
    else:
        raise Exception("select at least two items")


# these are option for type of constraint
def parentConst(value):
    number, driver, driven = setList()
    print("driver : ", driver)
    print("driven : ", driven)
    for index in range(number):
        cmds.parentConstraint(driver[index], driven[index], mo = value)
    
    return


def pointConst(value):
    number, driver, driven = setList()
    print("driver : ", driver)
    print("driven : ", driven)
    for index in range(number):
        cmds.pointConstraint(driver, driven, mo = value)
    
    return


def orientConst(value):
    number, driver, driven = setList()
    print("driver : ", driver)
    print("driven : ", driven)
    for index in range(number):
        cmds.orientConstraint(driver, driven, mo = value)
    
    return


def scaleConst(value):
    number, driver, driven = setList()
    print("driver : ", driver)
    print("driven : ", driven)
    for index in range(number):
        cmds.scaleConstraint(driver, driven, mo = value)
    
    return

