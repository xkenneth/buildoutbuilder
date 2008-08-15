import grok

def get_application(context):
    obj = context
    while not isinstance(obj, grok.Application):
        obj = obj.__parent__
    return obj
