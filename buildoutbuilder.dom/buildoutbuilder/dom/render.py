import pdb
import ConfigParser
import StringIO

from lxml import etree

### APP ###
from generate import generate
from testCase import DOMTestCase

def to_string(cp):
    t = StringIO.StringIO()
    cp.write(t)
    t.seek(0)
    return t.read()

def render(dom):
    """Returns a ConfigParser instance from a buildout DOM"""
    
    parts = []

    cp = ConfigParser.ConfigParser()
    
    for part in dom:

        if part.tag != 'buildout': parts.append(part.tag)
        cp.add_section(part.tag)
        
        for option in part:
            values = []
            for sub_option in option:
                if (len(sub_option)>0):
                    for sub in sub_option:
                        values.append(render_link(sub))
                else:
                    values.append(sub_option.text)
            
            cp.set(part.tag,option.tag,render_list(values))
            
    

    cp.set('buildout','parts',render_list(parts))


    return cp



def render_link(dom):
    """Return a string representation of a buildout_link"""

    section = dom.xpath('./section')[0]
    option = dom.xpath('./option')[0]
    
    return '${'+str(section.text)+':'+str(option.text)+'}'

def render_list(values):
    val_str = ''
    last = None
    for val in values:
        if last is None:
            val_str += val
        else:
            val_str += '\n' + val
        last = val

    return val_str
            
