import re
from buildoutbuilder.managers.Link import Link
from buildoutbuilder.managers.Link import link_re_capture
from buildoutbuilder.managers.errors import *
private_re = re.compile('__.*__')

class PartManager:
    def __init__(self,section_name,options_dict):
        """Initiates a partManager object from a dictionary of options"""

        #a new container
        options = {}

        #for every incoming option
        for option in options_dict:
            try:
                #make sure it's not __private__
                private_re.search(option).group()
                
            except AttributeError:
                #if not, add it to our new container
                options[option] = options_dict[option]
        
        
        
        #do i need this?
        #check to make sure that we've got a recipe
        #try:
        #    options['recipe']
        #except KeyError:
        #    raise PartIsNotRecipe(section_name)
        
        
        #find and create the links
        for option in options:
            #initial split to seperate lists
            options[option] = options[option].split() 

            for sub_option in options[option]:
                #try to see if the sub_option contains a link
                sub_option_split = link_re_capture.split(sub_option)
                

                for sub_part in sub_option_split:
                    try:
                        new_link = Link(sub_part)
                        sub_option_split[sub_option_split.index(sub_part)] = new_link
                    except ValueError:
                        pass
                    
                try:
                    while (1):
                        sub_option_split.pop(sub_option_split.index(''))
                except ValueError:
                    pass

                options[option][options[option].index(sub_option)] = sub_option_split
                    
                    
                #if it does
                # if new_link is not None:
#                     #check to see if it's only a link
#                     if sub_option == new_link.render():
#                         options[option][options[option].index(sub_option)] = new_link
#                     else:
#                         no_link = sub_option.split(new_link.render())
#                         if no_link[0] == '':
#                             init = 0
#                         else:
#                             init = 1
#                         for i in range(len(no_link)-1):
#                             no_link.insert(init+2*i,new_link)
                            
#                         try:
#                             while (1):
#                                 no_link.pop(no_link.index(''))
#                         except ValueError:
#                             pass
                        
#                         options[option][options[option].index(sub_option)] = no_link

                        
                  
        self.options = options
        
        self.section_name = section_name
        
        
            
        
    def render(self,config_parser):
        config_parser.add_section(self.section_name)

        def render_recursive(option,depth=0):
            if isinstance(option,str):
                return option
            try:
                render_str = ''
                for opt in option:
                    render_str += render_recursive(opt,depth=depth+1)
                    if opt != option[-1] and depth == 0:
                        render_str += '\n'
                return render_str
            except TypeError:
                return option.render()
                

        for option in self.options:

            result = render_recursive(self.options[option])

            config_parser.set(self.section_name,option,result)
        

    def __repr__(self):
        return self.section_name

if __name__ == '__main__':
    import unittest
    class PartManagerTests(unittest.TestCase):
        def setUp(self):
            self.test_section_name = 'zope'
            self.test_section_bad_dict = {'option':'value'}
            self.test_section_good_dict = {'recipe':'value',
                                           'option':'value'}
            self.test_link_section_name = 'config'
            self.test_link_section_option = 'namespace'
            self.test_link_section_option_2 = 'package'
            self.single_link_str = '${'+self.test_link_section_name+':'+self.test_link_section_option+'}'
            self.single_link_str_2 = '${'+self.test_link_section_name+':'+self.test_link_section_option_2+'}'
            self.test_single_link = {'recipe':self.single_link_str}
            self.assembled_single_link = Link(self.single_link_str)

            self.test_multiple_link = {'recipe':self.single_link_str+'.'+self.single_link_str_2}

        def testSetup(self):
            pass
        def testBadDict(self):
            try:
                pm = PartManager(self.test_section_name,self.test_section_bad_dict)
                self.fail()
            except KeyError:
                pass
        def testGoodDict(self):
            pm = PartManager(self.test_section_name,self.test_section_good_dict)
        def testSignleLink(self):
            pm = PartManager(self.test_section_name,self.test_single_link)
            self.failUnlessEqual(pm.options['recipe'][0],self.assembled_single_link)
        def testMultipleLink(self):
            print self.test_multiple_link
            pm = PartManager(self.test_section_name,self.test_multiple_link)
            print pm.options

    unittest.main()
        
        
        
