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

	cp.set('zope','alink','${this:that}')
	
	return cp

def buildout5():
	"""Add some eggs."""
	cp = buildout4()

	cp.set('buildout','eggs','buildoutbuilder')

	return cp

def buildout6():
	"""Add some find-links."""
	cp = buildout5()
	
	cp.set('buildout','find-links','http://pypi.python.org')
	
	return cp

def buildout7():
	"""Add an item that has a composite link"""
	cp = buildout6()

	cp.set('zope','eggs','${buildout:packages}/some/dir')
	
	return cp

def buildout8():
	"""Add a doubley composite link"""
	cp = buildout7()

	return cp

def buildout9():
	"""Add an option with multiple values"""
	cp = buildout8()
	
	cp.set('zope','paths','/usr/bin\n/usr/local')
	
	return cp




buildouts = [buildout1(),
	     buildout2(),
	     buildout3(),
	     buildout4(),
	     buildout5(),
	     buildout6(),
	     buildout7(),
	     buildout8(),
	     buildout9()]


