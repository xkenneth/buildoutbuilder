### Tests ###
import unittest
from generate import generate
from render import render, to_string
from lxml import etree


class ThereAndBack(unittest.TestCase):
    def setUp(self):
        from buildouts import buildouts
        self.buildouts = buildouts

    def testAll(self):
        for buildout in self.buildouts:
            buildout_string = to_string(buildout)
            generated_buildout = to_string(render(generate(buildout)))
            if buildout_string != generated_buildout:
                print "Test Case Failure!"
                print "Input"
                print etree.tostring(generate(buildout),pretty_print=True)
                print buildout_string
                print ""
                print "!="
                print "Generated"
                print 
                print generated_buildout
                self.fail()
            

if __name__ == '__main__':
    #run
    unittest.main()

