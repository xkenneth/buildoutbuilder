import grok
import pdb
import os.path
import dircache
import re
import tarfile
import cStringIO


from megrok.kss import KSSActions

from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.schema import TextLine

from buildoutbuilder.managers.BuildoutManager import BuildoutManager
from buildoutbuilder.managers.errors import *
from buildoutbuilder.grokapp import utils

#viewlet managers
from buildoutbuilder.grokapp.viewletmanagers import MainContent, Header, LeftSidebar

from persistent.mapping import PersistentMapping

#custom containers and models
from buildoutbuilder.grokapp.buildout import Buildout

#constants
BUILDOUTS_FOLDER = 'buildouts'

#re's for checking files
buildout_re = re.compile('.*.cfg$')
tar_re = re.compile('.*.tar.gz')

#main app
class BuildoutBuilder(grok.Application, grok.Container):
    pass

#container for buildouts
class BuildoutContainer(grok.Container):
    pass

#buildout model

#buildout indexes


    
#main content viewlet manager


#css

#app
class AppCSS(grok.Viewlet):
    grok.viewletmanager(Header)
    grok.context(Interface)

#rounded corners
class RoundedCornersCSS(grok.Viewlet):
    grok.viewletmanager(Header)
    grok.context(Interface)


#kss
class AppKSS(KSSActions):
    grok.context(BuildoutBuilder)
    def presentFindLinkForm(self):
        new_find_link_form = """<form><input type="text" name="newfindlink"><input type="submit" value="Add" id="add_find_link_submit"></form>"""

        core = self.getCommandSet('core')
        core.replaceHTML('#show_add_find_link_form', new_find_link_form)
    
    def addFindLink(self):
        pass
        #for field, value in self.request.form.items():
        #   if field == u'newfindlink':
        #        self.context.buildoutmanager.find_links.append(value)
        #print self.context

#views
class Index(grok.View):
    grok.context(BuildoutBuilder)
    def update(self):
        pass
    
    

class CreateBuildout(grok.View):
    grok.context(BuildoutBuilder)
    grok.template('index')

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
        try:
            self.context['preconfigured']
        except KeyError:
            self.context['preconfigured'] = BuildoutContainer()
            
        for toplevel in valid_buildouts:
            for buildout in toplevel['buildouts']:
                try:
                    self.context['preconfigured'][unicode(buildout['uid'])] = Buildout(buildout['manager'])
                except Exception, e:
                    print e

#viewlets

#buildout viewlets


#header viewlets
class Title(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Header)
    grok.order(1)

class Menu(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Header)
    grok.order(2)

#content viewlets
class Intro(grok.Viewlet):
    grok.viewletmanager(MainContent)
    grok.context(BuildoutBuilder)
    grok.view(Index)
    
    #def render(self):
    #    return 'Hello!'

class EditBuildout(grok.Viewlet):
    grok.viewletmanager(MainContent)
    grok.context(BuildoutBuilder)
    grok.view(CreateBuildout)
    grok.template('buildoutview')

    buildout_editable = True
    
    def update(self):
        pass

class BuildoutView(grok.Viewlet):
    grok.viewletmanager(MainContent)
    grok.context(BuildoutBuilder)
    grok.view(Buildouts)

    buildout_editable = False
    
    def update(self):
        buildout_uid = self.__parent__.buildout
        buildouts = self.__parent__.buildouts
        
        buildout = None
        count = 0

        self.buildoutmanager = None

        if buildout_uid is not None:
            for toplevel in buildouts:
                #for every buildout
                for bo in toplevel['buildouts']:
                    if int(bo['uid']) == int(buildout_uid):
                        buildout = bo
                        break
            
            self.buildoutmanager = buildout['manager']

            
        

class BuildoutList(grok.Viewlet):
    grok.viewletmanager(LeftSidebar)
    grok.order(1)
    grok.context(BuildoutBuilder)
    grok.view(Buildouts)

    def update(self):
        self.buildouts = self.__parent__.buildouts

#left viewlets
class LeftPaneIntro(grok.Viewlet):
    grok.viewletmanager(LeftSidebar)
    grok.order(1)
    grok.context(BuildoutBuilder)
    grok.view(Index)




