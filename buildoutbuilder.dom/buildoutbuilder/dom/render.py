from generate import generate

def render(dom):
    pass

if __name__ == '__main__':
    
    import unittest
    class Reconstruction(DOMTestCase):
        def testBuildout1(self):
            print render(generate(self.buildout1))

    unittest.main()
    
    
