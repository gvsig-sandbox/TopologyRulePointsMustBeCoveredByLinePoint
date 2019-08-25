# encoding: utf-8

import gvsig
import sys

from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.fmap.geom import Geometry
from org.gvsig.tools.util import ListBuilder
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRuleFactory

from pointsMustBeCoveredByLinePointRule import PointsMustBeCoveredByLinePointRule

class PointsMustBeCoveredByLinePointRuleFactory(AbstractTopologyRuleFactory):
      
    def __init__(self):
        AbstractTopologyRuleFactory.__init__(
            self,
            "PointsMustBeCoveredByLinePoint",
            "Points Must Be Covered By Line Point Rule",
            "This rule requires that the point in on layer must be covered by lines in another layer so points errors are created on the points that are not covered by lines.",
            ListBuilder().add(Geometry.TYPES.POINT).add(Geometry.TYPES.MULTIPOINT).asList(),
            ListBuilder().add(Geometry.TYPES.CURVE).add(Geometry.TYPES.MULTICURVE).asList()
        )
    
    def createRule(self, plan, dataSet1, dataSet2, tolerance):
        rule = PointsMustBeCoveredByLinePointRule(plan, self, tolerance, dataSet1, dataSet2)
        return rule

def selfRegister():
    try:
        manager = TopologyLocator.getTopologyManager()
        manager.addRuleFactories(PointsMustBeCoveredByLinePointRuleFactory())
    except:
        ex = sys.exc_info()[1]
        gvsig.logger("Can't register rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass
