import grok
import pdb
import os.path
import dircache
import re

from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.schema import TextLine

from buildoutbuilder.managers.BuildoutManager import BuildoutManager

BUILDOUTS_FOLDER = 'buildouts'

buildout_re = re.compile('.*.cfg$')

#grok.context(Interface) #not sure what this line does? -KCM

def get_application(context):
    obj = context
    while not isinstance(obj, BuildoutBuilder):
        obj = obj.__parent__
    return obj

class BuildoutBuilder(grok.Application, grok.Container):
    pass

#header viewlet manager
class Header(grok.ViewletManager):
    grok.name('header')

#left side bar viewlet manager
class LeftSidebar(grok.ViewletManager):
    grok.name('left')

#main content viewlet manager
class MainContent(grok.ViewletManager):
    grok.name('main')

#main app css
class AppCSS(grok.Viewlet):
    grok.viewletmanager(Header)
    grok.context(BuildoutBuilder)

class RoundedCornersCSS(grok.Viewlet):
    grok.viewletmanager(Header)
    grok.context(BuildoutBuilder)

class Title(grok.Viewlet):
    grok.viewletmanager(Header)
    grok.order(1)

class Menu(grok.Viewlet):
    grok.viewletmanager(Header)
    grok.order(2)

class Index(grok.View):
    pass

class Buildouts(grok.View):
    grok.context(BuildoutBuilder)
    grok.template('index')

    def update(self,buildout=None):
        self.buildout = buildout

        buildout_dir = self.static.get(BUILDOUTS_FOLDER).context.path
        valid_buildouts = []
        if os.path.isdir(buildout_dir):
            buildouts = dircache.listdir(buildout_dir)
            for bo in buildouts:
                #if it's a valid file
                if buildout_re.match(bo) is not None:
                    valid_buildouts.append({'buildout':bo[0:-4],
                                           'path':os.path.join(buildout_dir,bo),
                                           'url':self.url('buildouts')+'?buildout='+bo[0:-4]})

        self.buildouts = valid_buildouts
    
class Intro(grok.Viewlet):
    grok.viewletmanager(MainContent)
    grok.context(BuildoutBuilder)
    grok.view(Index)
    
    #def render(self):
    #    return 'Hello!'

class BuildoutView(grok.Viewlet):
    grok.viewletmanager(MainContent)
    grok.context(BuildoutBuilder)
    grok.view(Buildouts)

    def update(self):
        buildout_name = self.__parent__.buildout
        buildouts = self.__parent__.buildouts
        
        buildout = None
        count = 0

        self.manager = None

        if buildout_name is not None:
            while(buildout is None):
                if buildouts[count]['buildout'] == buildout_name:
                    buildout = buildouts[count]
                count += 1
            self.manager = BuildoutManager(buildout['path'])

            
        

class BuildoutList(grok.Viewlet):
    grok.viewletmanager(LeftSidebar)
    grok.order(1)
    grok.context(BuildoutBuilder)
    grok.view(Buildouts)

    def update(self):
        self.buildouts = self.__parent__.buildouts

class LeftPaneIntro(grok.Viewlet):
    grok.viewletmanager(LeftSidebar)
    grok.order(1)
    grok.context(BuildoutBuilder)
    grok.view(Index)




