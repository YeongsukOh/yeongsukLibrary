# question : is it possible to autoload instead of writing import module in everyScript?
# 라이브러리내의 하나의 팩키지에서 함수로 작성할 때와 클래스로 작성시의 장단점
import maya.cmds as cmds


# need some comment here
class ConstraintList():

    '''
    # Question! : where can I set up this script??
    sel = cmds.ls(sl = True)
    num = int(len(sel)/2)
    driver = sel[:num]
    driven = sel[num:]

    # need some comment here
    def __init__(self, driver, driven, maintainOffset):
        # checking how to writ attribute in a class
        self.maintainOffset = maintainOffset
        self.driver = driver
        self.driven = driven
        print(driver, driven)    
    # how can I add the common attribute for maintain offset


    # need some comment here
    def parentConstraint(self, maintainOffset):

        if not self.driver:
            raise Exception("There is no driver")
        elif not self.driven:
            raise Exception("There is no driven")
        else:
            pass 
        
        for index in range(self.num):
            cmds.parentConstraint(self.driver, self.driven, mo =maintainOffset)


    # need some comment here
    def pointConstraint(self, maintainOffset):
        return


    # need some comment here
    def orientConstraint(self, maintainOffset):
        return


    # need some comment here
    def scaleConstraint(self, maintainOffset):
        return
    '''