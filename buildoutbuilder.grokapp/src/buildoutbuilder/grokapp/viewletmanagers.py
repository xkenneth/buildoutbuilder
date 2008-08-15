import grok

from zope.interface import Interface

grok.templatedir('app')

class MainContent(grok.ViewletManager):
    grok.context(Interface)
    grok.name('main')

#header viewlet manager
class Header(grok.ViewletManager):
    grok.context(Interface)
    grok.name('header')

#left side bar viewlet manager
class LeftSidebar(grok.ViewletManager):
    grok.context(Interface)
    grok.name('left')
