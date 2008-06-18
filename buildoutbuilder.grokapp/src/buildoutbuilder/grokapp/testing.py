import os.path
import buildoutbuilder
from zope.app.testing.functional import ZCMLLayer

ftesting_zcml = os.path.join(
    os.path.dirname(buildoutbuilder.__file__), 'ftesting.zcml')
FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer')
