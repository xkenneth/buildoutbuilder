import grok
import pdb
#access to app modules
pdb.set_trace()
from app import MainContent

#set the template directory
grok.templatedir('app')


##### MODELS #####
class Buildout(grok.Model):
    def __init__(self,manager):
        #a manager represents a buildout
        self.manager = manager

##### VIEWS #####
class Index(grok.View):
    grok.context(Buildout)
    grok.template('index')
    grok.name('index')

    def update(self):
        #pdb.set_trace()
        pass


##### VIEWLETS #####
class BuildoutContent(grok.Viewlet):
    grok.viewletmanager(MainContent)
    grok.context(Buildout)
    grok.template('buildoutview')
