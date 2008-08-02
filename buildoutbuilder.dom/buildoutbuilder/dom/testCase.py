import unittest
import pdb
from ConfigParser import ConfigParser
from StringIO import StringIO

def buildout2():
	cp = ConfigParser()
	cp.add_section('buildout')
	cp.set('buildout','parts','')
	t = StringIO('')
	cp.write(t)
	t.seek(0)
	return t.read()

buildouts = [buildout2()]

class DOMTestCase(unittest.TestCase):
    def setUp(self):
        self.buildout1 = """[buildout]
parts = test
eggs = test
develop = .
find-links = pypi.python.org
[test]
option = value
option2 = ${buildout:eggs}
option3 = test
    test1
    test2
"""
	    
	self.buildout2 = buildout2()

	self.garbage = "askdfjdskf;asdflkasnglj;afg"


    def tearDown(self):
        pass

    def testBasics(self):
        print self.buildout2

if __name__ == '__main__':
    unittest.main()
