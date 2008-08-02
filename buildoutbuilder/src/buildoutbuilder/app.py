import grok
import pdb
import os.path
import dircache
import re
import tarfile
import cStringIO

from lxml import etree

### ZOPE ###
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.schema import TextLine

### MEGROK ###

### CONSTANTS ###
BUILDOUTS_FOLDER = 'buildouts'

### RES ###
buildout_re = re.compile('.*.cfg$')
tar_re = re.compile('.*.tar.gz')
cfg_re = re.compile('.*.cfg')

#IN MEMORY ONLY
BUILDOUTS = []

#helper functions
def assemble_list(l,delim):
    s = ''
    first = True
    for i in l:
        if first:
            s += i
        else:
            s += delim + i

        first = False

    return s

class Buildoutbuilder(grok.Application, grok.Container):
    pass

class Index(grok.View):
    pass # see app_templates/index.pt

### XML-RPC ###
class BuildoutbuilderXMLRPC(grok.XMLRPC):
    def buildout_dom(self,dom):
        print dom
        print self.context
        pdb.set_trace()
        return True

    def test(self):
        return True

### VIEWS ###
        

class Buildouts(grok.View):
    """Renders a DOM representing the available buildouts."""
    def render(self):
        #updating the current buildout view uid
        self.response.setHeader('Content-Type', 'text/xml')

        dom = etree.Element('Buildouts')

        buildout_dir = self.static.get(BUILDOUTS_FOLDER).context.path

        pdb.set_trace()
        
        valid_buildouts = []
        if os.path.isdir(buildout_dir):
            uid = 0
            buildouts = dircache.listdir(buildout_dir)


            for buildout in buildouts:
                if tar_re.match(buildout) is not None:
                    buildout_files = []
                    tar = tarfile.open(os.path.join(buildout_dir,buildout), "r:gz")
                    for f in tar:
                        if buildout_re.match(f.name) is not None:
                            try:
                                buildout_files.append({'tar':tar,
                                                       'directory':'t',
                                                       'file':f,
                                                       'dom': None,
                                                       'filename':f.name,
                                                       'uid':uid,
                                                       'url':self.url('buildouts')+'?buildout='+str(uid)})
                                
                                
                                uid += 1
                            except BuildoutBuilderException, e:
                                #see if it's a BB exc
                                #if isinstance(e,BuildoutBuilderException):
                                
                                pass
                                #else:
                                #    raise e
                            except Exception, e:
                                print e
                            
                            
                    if tar_re.match(buildout):
                        buildout = assemble_list(buildout.split('.')[0:-2],'.')

                    valid_buildouts.append({'toplevel':buildout,
                                            'buildouts':buildout_files})
                    
                #self.context.buildouts = valid_buildouts
                BUILDOUTS.extend(valid_buildouts)

        ### Generate the DOM tree representing the buildouts ###
        for valid_buildout in valid_buildouts:
            #for each toplevel (tar.gz)
            toplevel = etree.Element('toplevel')
            #set the name
            toplevel.set('name',valid_buildout['toplevel'].split()[0])
            
            #for each buildout
            for buildout in valid_buildout['buildouts']:
                tree = '/toplevel'
                last = tree
                for name in buildout['filename'].split('/')[1:]:
                    next = 'node'
                    #if cfg_re.match(name): 
                    #    next = 'file'

                    tree += '/' + next + "[@name='" + name + "']"

                    print tree

                    if len(toplevel.xpath(tree)) == 0:
                        parent = toplevel.xpath(last)[0]

                        new_element = etree.Element('node')
                        if cfg_re.match(name):
                            new_element.set('file','true')
            
                        new_element.set('name',name)
                        parent.append(new_element)
                    
                    last = tree
                        
                        

                
                
                
                
                
                
            dom.append(toplevel)
            
        print etree.tostring(dom,pretty_print=True)
        return etree.tostring(dom,pretty_print=True)
