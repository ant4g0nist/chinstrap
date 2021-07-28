## Copyright 2019-2020 Smart Chain Arena LLC. ##

import subprocess
import os


class SmartmlCtx:
    def call(self, f, *args):
        def pp(x):
            if isinstance(x, str):
                return "'%s'" % x
            else:
                return str(x)

        # print ("  Calling %s(%s)" % (f, ', '.join(pp(x) for x in args)))
        return None

class SmartpyContext:
    contractNextId = 0
    
    def nextId(self):
        result = self.contractNextId
        self.contractNextId += 1
        return result

    def clearOutputs():
        return

    def setOutput(self, s):
        setOutput(s)

    def addOutput(self, s):
        pass

class Window:
    pythonTests = []
    smartmlCtx = SmartmlCtx()
    smartpyContext = SmartpyContext()
    in_browser = False
    lambdaNextId = 0
    activeTrace = None

    class console: pass
    console.log = print

class Document:
    pass


window = Window()
document = Document()


def alert(x):
    print("ALERT" + str(x))


scenario = []


def setOutput(l):
    global scenario
    scenario = l
