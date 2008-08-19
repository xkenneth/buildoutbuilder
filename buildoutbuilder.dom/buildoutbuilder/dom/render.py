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
        
        if part.get('name') != 'buildout': parts.append(part.get('name'))
        cp.add_section(part.get('name'))
        
        for option in part:
            values = []
    
            for sub_option in option:
                sub_values = []
                for sub in sub_option:
                    if sub.tag == 'link':
                        sub_values.append(render_link(sub))
                    else:
                        sub_values.append(sub.text)
                
                values.append(render_list(sub_values))
            
            cp.set(part.get('name'),option.get('name'),render_list(values,delim='\n'))
            
    

    if cp.has_section('buildout'):
        cp.set('buildout','parts',render_list(parts,delim="\n"))

    return cp



def render_link(dom):
    """Return a string representation of a buildout_link"""

    section = dom.xpath('./section')[0]
    option = dom.xpath('./option')[0]
    
    return '${'+str(section.text)+':'+str(option.text)+'}'

def render_list(values, delim=''):
    val_str = ''
    last = None
    for val in values:
        if last is None:
            val_str += val
        else:
            val_str += delim + val
        last = val

    return val_str
            
if __name__ == '__main__':
    from buildouts import buildouts
    from generate import generate
    
    
    print to_string(render(generate(buildouts[-1])))
    
