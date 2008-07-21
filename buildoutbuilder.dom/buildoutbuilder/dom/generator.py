import lxml
import ConfigParser
import pdb

def generator(buildout):
    cp = ConfigParser.ConfigParser()
    cp.read(buildout)

    pdb.set_trace()

    pass

if __name__ == '__main__':
    import unittest
    
    class Basics(unittest.TestCase):
        def setUp(self):
            self.buildout1 = """
[buildout]
parts = 
"""
            self.garbage = "askdfjdskf;asdflkasnglj;afg"


        def tearDown(self):
            pass

    class Construction(Basics):
        def testBuildout1(self):
            print generator(self.buildout1)
            
    unittest.main()
