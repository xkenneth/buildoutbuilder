import re

link_re = re.compile('\${[^\{^\}]*}')
link_re_capture = re.compile('(\${[^\{^\}]*})')

class Link:
    def __init__(self,option):
        #match the link
        try:
            link = link_re.search(option).group()
        except AttributeError:
            #then it's not a link, and raise a competent error
            raise ValueError('Option does not contain a link',option)

        #seperate the section and option
        self.section,self.option = link[2:len(link)-1].split(':')
        

    def __repr__(self):
        return "${ " + self.section + " : " + self.option + " }"

    def render(self):
        return "${" + self.section + ":" + self.option + "}"
    
    def __eq__(self,other):
        if not isinstance(other,Link):
            return NotImplemented

        return self.section == other.section and self.option == other.option

    def __ne__(self,other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
        

if __name__ == '__main__':
    import unittest
    class LinkUnitTests(unittest.TestCase):
        def setUp(self):
            self.link = '{section:option}'
            self.tests = []
            self.tests.append('asdfabgsdfg' + self.link + 'asfabdmbdfgf')
            self.tests.append('{' + self.link + '}')
            self.garbage = 'afsdfnsvjbfdsa'
        def tearDown(self):
            pass
        def testRE(self):
            for test in self.tests:
                self.failUnlessEqual(self.link,link_re.search(test).group())
        def testInst(self):
            for test in self.tests:
                Link(test)
        def testGarbage(self):
            try:
                Link(self.garbage)
                self.fail()
            except ValueError:
                pass
    unittest.main()
