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

def buildout3():
	"""Testing some options."""
	cp = buildout2()
	cp.set('zope','instance','fg')
	
	return cp

def buildout4():
	"""Setting up some links."""
	cp = buildout3()
	
	return cp

def buildout5():
	"""Add some find-links."""
	cp = buildout4()
	
	return cp

def buildout6():
	"""Add some eggs."""
	cp = buildout5()
	return cp


buildouts = [buildout1(),buildout2(),buildout3(),buildout4(),buildout5(),buildout6()]

