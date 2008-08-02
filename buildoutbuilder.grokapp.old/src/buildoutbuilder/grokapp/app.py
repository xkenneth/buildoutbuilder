import grok
import pdb
import os.path
import dircache
import re
import tarfile
import cStringIO

### ZOPE ###
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.schema import TextLine

### MEGROK ###
from megrok.kss import KSSActions

### PACKAGE ###
from buildoutbuilder.managers.BuildoutManager import BuildoutManager
from buildoutbuilder.managers.errors import *
from buildoutbuilder.grokapp import utils

### APP ###
from viewletmanagers import MainContent, Header, LeftSidebar
from buildout import Buildout

### CONSTANTS ###
BUILDOUTS_FOLDER = 'buildouts'


### RES ###
buildout_re = re.compile('.*.cfg$')
tar_re = re.compile('.*.tar.gz')

#class AppKSS(KSSActions):
#    def newDevelopDir(self):
#        core = self.getCommandSet('core')
#        core.replaceHTML('#new_develop_dir', '<p>ME GROK KISSED !</p>')

class BuildoutBuilder(grok.Application, grok.Container):
    pass

#main app css
#class AppCSS(grok.Viewlet):
#    grok.viewletmanager(Header)
#    grok.context(BuildoutBuilder)

#class RoundedCornersCSS(grok.Viewlet):
#    grok.viewletmanager(Header)
#    grok.context(BuildoutBuilder)

#class Title(grok.Viewlet):
#    grok.viewletmanager(Header)
#    grok.order(1)

#class Menu(grok.Viewlet):
#    grok.viewletmanager(Header)
#    grok.order(2)

class Index(grok.View):
    def update(self):
        try:
            self.context['test'] = Buildout(0)

        except Exception, e:
            print e
        
class Buildouts(grok.View):
    grok.context(BuildoutBuilder)
    grok.template('index')

    def update(self,buildout=None):
        #updating the current buildout view uid
        self.buildout = buildout

        buildout_dir = self.static.get(BUILDOUTS_FOLDER).context.path
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
                                manager = BuildoutManager(tar.extractfile(f.name).read())
                                buildout_files.append({'tar':tar,
                                                       'directory':'t',
                                                       'file':f,
                                                       'filename':f.name,
                                                       'uid':uid,
                                                       'url':self.url('buildouts')+'?buildout='+str(uid),
                                                       'manager':manager})
                                
                                
                                uid += 1
                            except BuildoutBuilderException, e:
                                #see if it's a BB exc
                                #if isinstance(e,BuildoutBuilderException):
                                
                                pass
                                #else:
                                #    raise e
                            except Exception, e:
                                print e
                            
                            
                    
                    valid_buildouts.append({'toplevel':buildout,
                                            'buildouts':buildout_files})
        self.buildouts = valid_buildouts

        pdb.set_trace()
    
# class Intro(grok.Viewlet):
#     grok.viewletmanager(MainContent)
#     grok.context(BuildoutBuilder)
#     grok.view(Index)
    
#     #def render(self):
#     #    return 'Hello!'

# class BuildoutView(grok.Viewlet):
#     grok.viewletmanager(MainContent)
#     grok.context(BuildoutBuilder)
#     grok.view(Buildouts)

#     def update(self):
#         buildout_uid = self.__parent__.buildout
#         buildouts = self.__parent__.buildouts
        
#         buildout = None
#         count = 0

#         self.manager = None

#         if buildout_uid is not None:
#             for toplevel in buildouts:
#                 #for every buildout
#                 for bo in toplevel['buildouts']:
#                     if int(bo['uid']) == int(buildout_uid):
#                         buildout = bo
#                         break
            
#             self.manager = buildout['manager']

            
        

# class BuildoutList(grok.Viewlet):
#     grok.viewletmanager(LeftSidebar)
#     grok.order(1)
#     grok.context(BuildoutBuilder)
#     grok.view(Buildouts)

#     def update(self):
#         self.buildouts = self.__parent__.buildouts

# class LeftPaneIntro(grok.Viewlet):
#     grok.viewletmanager(LeftSidebar)
#     grok.order(1)
#     grok.context(BuildoutBuilder)
#     grok.view(Index)




