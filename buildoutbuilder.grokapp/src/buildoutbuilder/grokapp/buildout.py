import grok
import pdb

from megrok.kss import KSSActions

### ZOPE ###
from zope.formlib import form
from zope.interface import Interface
from zope.publisher.browser import TestRequest
from zope import schema

### PACKAGE ###
from buildoutbuilder.managers.BuildoutManager import BuildoutManager

### APP ###
from viewletmanagers import MainContent, Header, LeftSidebar



grok.templatedir('app_templates')

### HELPER FUNCTIONS ###
def get_form_html(new_form):
    request = TestRequest()
    html = new_form(None, request)()
    return html

def wrapper(new_form):
    html = '<div id=%s>' % new_form.name
    html += get_form_html(new_form)
    html += '<div id=%s> Done </div></div>' % ( new_form.name + '.submit' )
    print html
    return html

class AppKSS(KSSActions):
    def newDevelopDir(self):
        core = self.getCommandSet('core')
        core.replaceHTML('#new_develop_dir',wrapper(DevelopDirForm))


class Buildout(grok.Model):
    """A grok.Model for a buildout"""

    def __init__(self, id, manager = None):
        """ID - Int, manager - buildoutmanager."""

        if manager is None:
            self.manager = BuildoutManager()
        else:
            self.manager = manager

        super(grok.Model, self).__init__()

class Index(grok.View):
    grok.context(Buildout)
    
class Debug(grok.View):
    grok.context(Buildout)
    grok.template('index')
    
    def update(self):
        pdb.set_trace()

class IDevelopDir(Interface):
    dir = schema.TextLine(title=u"Directory:")

class MyForm:
    name = 'form'
    def __init__(self, context, request):
        self.context, self.request = context, request

    def __call__(self, ignore_request=False):
        widgets = form.setUpWidgets(
            self.form_fields, self.name, self.context, self.request,
            ignore_request=ignore_request)
        return '\n'.join([w() for w in widgets])

class DevelopDirForm(MyForm):
    form_fields = form.Fields(IDevelopDir)
    name = 'develop_dir_form'
    

    

class BuildoutView(grok.Viewlet):
    """grok.viewlet to display the buildout"""
    grok.viewletmanager(MainContent)
    grok.order(0)
    grok.view(Index)
    

