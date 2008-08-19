import re
import StringIO
import os

from lxml import etree

import ConfigParser
import pdb

### APP ###
from testCase import DOMTestCase

#regular expressions
private_re = re.compile('__.*__')
link_re = re.compile('\${[^\{^\}]*}')
link_re_capture = re.compile('(\${[^\{^\}]*})')
split_value_re = re.compile('\$\{[^\}]*\}|[^\$^\{^\}]+')

def generate(uri):
    """Return an lxml.etree object that represents a buildout."""
    
    #initialize a configparser
    if isinstance(uri,ConfigParser.ConfigParser):
        cp = uri
        
    if isinstance(uri,str):
        cp = ConfigParser.ConfigParser()
        if (os.path.isfile(uri)):
            cp.read(uri)
        else:
            uri = StringIO.StringIO(uri)
            cp.readfp(uri)

        
    #if not already defined
    try:
        cp
    except NameError:
        cp = ConfigParser.ConfigParser()
        cp.read(uri)

    #if not cp.has_section( 'buildout' ):
    #    raise ValueError( 'Buildout does not have a buildout section' )
    
    tag_name = 'buildout'
    if not cp.has_section( 'buildout' ):
        tag_name = 'recipe'

    dom = etree.Element( tag_name )

    #get the sections from the configParser
    sections = cp._sections.keys()
    #we don't need th buildout section
    #sections.pop( cp._sections.keys().index( 'buildout' ) )
    
    #create the buildout element
    #buildout_element = etree.Element('part')
    #buildout_element.set('name','buildout')
    
    #for each part
    for section in sections:
        dom.append(generate_section(section,cp._sections[section]))

    #get and find all of the eggs
        #if the eggs are specified, is this mandatory?
    # if cp.has_option('buildout','eggs'):
#         #for every defined egg
#         eggs = etree.Element('option')
#         eggs.set('name','eggs')
#         for egg_name in cp.get('buildout','eggs').split():
#             egg = etree.Element('egg')
#             egg.text = egg_name
#             eggs.append(egg)
#         buildout_element.append(eggs)

        
    #get and find all of the find-links
    # if cp.has_option('buildout','find-links'):
#         find_links = etree.Element('option')
#         find_links.set('name','find-links')
#         for link_name in cp.get('buildout','find-links').split():
#             find_link = etree.Element('value')
#             find_link.text = link_name
#             find_links.append(find_link)
#         buildout_element.append(find_links)

    #get all of the dev dirs
#     if cp.has_option('buildout','develop'):
#         develop_dirs = etree.Element('option')
#         develop_dirs.set('name','develop')
#         for develop_dir in cp.get('buildout','develop').split():
#             directory = etree.Element('value')
#             directory.text = develop_dir
#             develop_dirs.append(directory)
#         buildout_element.append(develop_dirs)
            
    #dom.append(buildout_element)
    
    return dom

def generate_section(section,options_dict):

    #a new container
    options = {}
    
    #create the dom
    dom = etree.Element('part')
    dom.set('name',section)

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
        new_option = etree.Element('option')
        new_option.set('name',option)
        for each_value in options[option]:
            #see if it's a link
            new_value = etree.Element('value')
            for split_value in split_value_re.findall(each_value):
                
                try:
                    new_link = etree.Element('link')
                    link = link_re.search(split_value).group()
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
                    new_text = etree.Element('text')
                    new_text.text = split_value
                    new_value.append(new_text)
            new_option.append(new_value)

        dom.append(new_option)

    return dom
            
                

if __name__ == "__main__":
    from buildouts import buildouts
    
    
    print etree.tostring(generate(buildouts[-1]),pretty_print=True)
