# encoding: utf-8

import gvsig
import sys

from gvsig import geom
from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRule

from deletePointAction import DeletePointAction

class PointsMustBeCoveredByLinePointRule(AbstractTopologyRule):
    
    geomName = None
    expression = None
    expressionBuilder = None
    
    def __init__(self, plan, factory, tolerance, dataSet1, dataSet2):
        AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1, dataSet2)
        self.addAction(DeletePointAction())
    
    def intersects(self, buffer1, theDataSet2):
        result = False
        if theDataSet2.getSpatialIndex() != None:
            for featureReference in theDataSet2.query(buffer1):
                feature2 = featureReference.getFeature()
                line2 = feature2.getDefaultGeometry()
                if buffer1.intersects(line2):
                    result = True
                    break
        else:
            if self.expression == None:
                manager = ExpressionEvaluatorLocator.getManager()
                self.expression = manager.createExpression()
                self.expressionBuilder = manager.createExpressionBuilder()
                store2 = theDataSet2.getFeatureStore()
                self.geomName = store2.getDefaultFeatureType().getDefaultGeometryAttributeName()
            self.expression.setPhrase(
                self.expressionBuilder.ifnull(
                    self.expressionBuilder.column(self.geomName),
                    self.expressionBuilder.constant(False),
                    self.expressionBuilder.ST_Intersects(
                        self.expressionBuilder.geometry(buffer1),
                        self.expressionBuilder.column(self.geomName)
                    )
                ).toString()
            )
            if theDataSet2.findFirst(self.expression) == None:
                result = True
        return result
    
    def check(self, taskStatus, report, feature1):
        try:
            point1 = feature1.getDefaultGeometry()
            tolerance1 = self.getTolerance()
            theDataSet2 = self.getDataSet2()
            geometryType1 = point1.getGeometryType()
            if geometryType1.getSubType() == geom.D2 or geometryType1.getSubType() == geom.D2M:
                if geometryType1.getType() == geom.POINT or geometryType1.isTypeOf(geom.POINT):
                    buffer1 = point1.buffer(tolerance1)
                    if not self.intersects(buffer1, theDataSet2):
                        report.addLine(self,
                            self.getDataSet1(),
                            self.getDataSet2(),
                            point1,
                            point1,
                            feature1.getReference(),
                            None,
                            -1,
                            -1,
                            False,
                            "The point is not covered by line.",
                            ""
                        )
                else:
                    if geometryType1.getType() == geom.MULTIPOINT or geometryType1.isTypeOf(geom.MULTIPOINT):
                        n1 = point1.getPrimitivesNumber()
                        for i in range(0, n1 + 1):
                            buffer1 = point1.getPointAt(i).buffer(tolerance1)
                            if not self.intersects(buffer1, theDataSet2):
                                report.addLine(self,
                                    self.getDataSet1(),
                                    self.getDataSet2(),
                                    point1,
                                    point1.getPointAt(i),
                                    feature1.getReference(), 
                                    None,
                                    i,
                                    -1,
                                    False,
                                    "The multipoint is not covered by line.",
                                    ""
                                )
            else:
                report.addLine(self,
                    self.getDataSet1(),
                    self.getDataSet2(),
                    point1,
                    point1,
                    feature1.getReference(),
                    None,
                    -1,
                    -1,
                    False,
                    "Unsupported geometry subtype.",
                    ""
                )
        except:
            ex = sys.exc_info()[1]
            gvsig.logger("Can't execute rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass
