import ConfigParser
from errors import *
import pdb
import os.path
import StringIO

class BuildoutManager:
    def __init__(self,uri=None):
        """Initializes a buildoutmanager from a buildout located by a URI"""
        
        from buildoutbuilder.managers.PartManager import PartManager
        from buildoutbuilder.managers.Egg import Egg
        
        if uri is not None:
            self.uri = uri #save the URI
        
        #a container for our eggs
        self.eggs = []

        #a container for the find-links
        self.find_links = []

        #a container for develop dirs
        self.develop_dirs = []
        
        #to keep track of the part managers
        self.parts = {}

        #start the configparser
        cp = ConfigParser.ConfigParser() 
        
        if uri is not None:
            files = cp.read(uri)
            
            try:
                files.index(uri)
            except ValueError:
                buffer = StringIO.StringIO(uri)
                cp.readfp(buffer)
        

            #check to make sure that a buildout section is present
            if not cp.has_section('buildout'):
                raise MissingPart('buildout')
            
            #get the sections from the configParser
            sections = cp._sections.keys()
            #we don't need th buildout section
            sections.pop(cp._sections.keys().index('buildout'))
        
            #for each part defined, create a partManagerObject
            for section in sections:
                self.parts[section] = PartManager(section,cp._sections[section])
        
            #get and find all of the eggs
            #if the eggs are specified, is this mandatory?
            if cp.has_option('buildout','eggs'):
                #for every defined egg
                for egg_name in cp.get('buildout','eggs').split():
                    self.eggs.append(Egg(egg_name)) #create and save the egg

            #get and find all of the find-links
            if cp.has_option('buildout','find-links'):
                for link_name in cp.get('buildout','find-links').split():
                    self.find_links.append(link_name)

            #get all of the dev dirs
            if cp.has_option('buildout','develop'):
                for develop_dir in cp.get('buildout','develop').split():
                    self.develop_dirs.append(develop_dir)
                                      
            
        
            self.cp = cp

    def render(self,uri):

        #a configParser to assemble the buildout
        rendered_buildout = ConfigParser.ConfigParser()
        
        #create the buildout section
        rendered_buildout.add_section('buildout')

        #a template part string
        parts_str = ''
        
        #for all of the parts
        for key in self.parts:
            #assemble the parts option for the buildout section
            parts_str += key + '\n'
            
            #render the individual part
            self.parts[key].render(rendered_buildout)

        #render the parts option of the buildout section
        rendered_buildout.set('buildout','parts',parts_str)

        #render the eggs option of the buildout section
        eggs_str = ''

        for egg in self.eggs:
            eggs_str += egg.name + '\n'

            
        rendered_buildout.set('buildout','eggs',eggs_str)

        #render the find_links option of the buildout section
        find_links_str = ''

        for find_link in self.find_links:
            find_links_str += find_link + '\n'
            
        rendered_buildout.set('buildout','find_links',find_links_str)

        #render the develop_dirs option of the buildout section
        develop_dirs_str = ''

        for develop_dir in self.develop_dirs:
            develop_dirs_str += develop_dir + '\n'
            
        rendered_buildout.set('buildout','develop',develop_dirs_str)

            
        rendered_buildout.write(uri)

        
        
        

if __name__ == '__main__':
    import sys
    uri = sys.argv[1]

    bm = BuildoutManager(uri)

    bm.render(file('/tmp/readme','w'))

    f = file('/tmp/readme','r')
    
    print f.read()
