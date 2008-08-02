### Tests ###
import unittest
from generate import generate
from render import render, to_string



class ThereAndBack(unittest.TestCase):
    def setUp(self):
        from buildouts import buildouts
        self.buildouts = buildouts

    def testAll(self):
        for buildout in self.buildouts:
            self.failUnlessEqual(to_string(buildout),to_string(render(generate(buildout))))
            

if __name__ == '__main__':
    #run
    unittest.main()

