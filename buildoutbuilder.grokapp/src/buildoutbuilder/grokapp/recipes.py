import os, sys, dircache
from lxml import etree
from buildoutbuilder.dom.generate import generate

def clean(l):
    new_l = []
    for i in l:
        if i != '':
            new_l.append(i)

    return new_l

def assemble(l):
    s = ''
    for i in l:
        s += str(i)
    return s

def retrieve_recipes(dir,dom=None):
    
    #if dom is None:
    #    dom = etree.Element('recipe')
    #    dom.set('name','Recipes')
    
    if os.path.isdir(dir):
        node = etree.Element('recipe')
        if dom is None:
            dom = node
        node.set('name',clean(dir.split('/'))[-1])
        for f in dircache.listdir(dir):
            retrieve_recipes(os.path.join(dir,f),node)
        dom.append(node)

    if os.path.isfile(dir):
        f = file(dir,'r')
        node = etree.Element('recipe')
        #node.set('name',assemble(clean(dir.split('/'))[-1].split('.')[0:-1]))
        node.set('name',clean(dir.split('/'))[-1])
        node.set('recipe','true')

        recipe_dom = None
        try:
            recipe_dom = etree.fromstring(f.read())
        except etree.XMLSyntaxError:
            f.seek(0)
            recipe_dom = generate(f.read())
        
        node.append(recipe_dom)
        if recipe_dom is not None:
            dom.append(node)

    return dom




if __name__ == '__main__':
    print etree.tostring(retrieve_recipes(sys.argv[1]),pretty_print=True)
