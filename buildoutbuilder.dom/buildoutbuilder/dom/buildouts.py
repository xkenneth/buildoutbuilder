import unittest
import pdb
from ConfigParser import ConfigParser
from StringIO import StringIO
from render import to_string

def buildout1():
	"""Testing a single section."""
	cp = ConfigParser()
	cp.add_section('buildout')
	cp.set('buildout','parts','')
	return cp

def buildout2():
	"""Testing Multiple Sections."""
	#starting from the previous buildout
	cp = buildout1()
	#defining the parts
	cp.set('buildout','parts','zope\nplone')
	#parts must be in the correct order
	cp.add_section('zope')
	cp.add_section('plone')

	
	return cp



buildouts = [buildout1(),buildout2()]

