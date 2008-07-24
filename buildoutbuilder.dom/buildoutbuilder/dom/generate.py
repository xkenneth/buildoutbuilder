import re
import StringIO

from lxml import etree

import ConfigParser
import pdb

### APP ###
from testCase import DOMTestCase

#regular expressions
private_re = re.compile('__.*__')
link_re = re.compile('\${[^\{^\}]*}')
link_re_capture = re.compile('(\${[^\{^\}]*})')

def generate(uri):
    """Return an lxml.etree object that represents a buildout."""
    
    #initialize a configparser
    cp = ConfigParser.ConfigParser()
    
    if isinstance(uri,str):
        uri = StringIO.StringIO(uri)
        cp.readfp(uri)
    else:
        cp.read(uri)
        
    
    if not cp.has_section( 'buildout' ):
        raise ValueError( 'Buildout does not have a buildout section' )
    
    dom = etree.Element( "buildout" )

    #get the sections from the configParser
    sections = cp._sections.keys()
    #we don't need th buildout section
    sections.pop( cp._sections.keys().index( 'buildout' ) )
    
    #create the buildout element
    buildout_element = etree.Element('buildout')
    
    #for each part
    for section in sections:
        dom.append(generate_section(section,cp._sections[section]))

    #get and find all of the eggs
        #if the eggs are specified, is this mandatory?
    if cp.has_option('buildout','eggs'):
        #for every defined egg
        eggs = etree.Element('eggs')
        for egg_name in cp.get('buildout','eggs').split():
            egg = etree.Element('egg')
            egg.text = egg_name
            eggs.append(egg)
        buildout_element.append(eggs)

        
    #get and find all of the find-links
    if cp.has_option('buildout','find-links'):
        find_links = etree.Element('find-links')
        for link_name in cp.get('buildout','find-links').split():
            find_link = etree.Element('find-link')
            find_link.text = link_name
            find_links.append(find_link)
        buildout_element.append(find_links)

    #get all of the dev dirs
    if cp.has_option('buildout','develop'):
        develop_dirs = etree.Element('develop')
        for develop_dir in cp.get('buildout','develop').split():
            directory = etree.Element('dir')
            directory.text = develop_dir
            develop_dirs.append(directory)
        buildout_element.append(develop_dirs)
            
    dom.append(buildout_element)

    return dom

def generate_section(section,options_dict):

    #a new container
    options = {}
    
    #create the dom
    dom = etree.Element(section)

    #for every incoming option
    for option in options_dict:
        try:
            #make sure it's not __private__
            private_re.search(option).group()
                
        except AttributeError:
            #if not, add it to our new container
            options[option] = options_dict[option].split()

        
    #find and create the links
    
    for option in options:
        new_option = etree.Element(option)
        for each_value in options[option]:
            #see if it's a link
            new_value = etree.Element('value')
            try:
                new_link = etree.Element('link')
                link = link_re.search(each_value).group()
                new_link_section = etree.Element('section')
                new_link_option = etree.Element('option')
                
                
                link_section,link_option = link[2:len(link)-1].split(':')
                new_link_section.text = link_section
                new_link_option.text = link_option
                new_link.append(new_link_section)
                new_link.append(new_link_option)
                new_value.append(new_link)
            except AttributeError:
                #then it's not a link!
                new_value.text = each_value
            new_option.append(new_value)

        dom.append(new_option)

    return dom
            
                

    #for option in options:
#         #initial split to seperate lists
#         options[option] = options[option].split() 

#         for sub_option in options[option]:
#             #try to see if the sub_option contains a link
#             sub_option_split = link_re_capture.split(sub_option)
                
            
#             for sub_part in sub_option_split:
#                 try:
#                     pdb.set_trace()
#                     new_link = sub_part
#                     sub_option_split[sub_option_split.index(sub_part)] = new_link
#                 except ValueError:
#                     pass
                    
#             try:
#                 while (1):
#                     sub_option_split.pop(sub_option_split.index(''))
#             except ValueError:
#                 pass

#             options[option][options[option].index(sub_option)] = sub_option_split
            
if __name__ == '__main__':
    import unittest

    class Construction(DOMTestCase):
        def testBuildout1(self):
            print etree.tostring(generate(self.buildout1),pretty_print=True)
            
    unittest.main()
