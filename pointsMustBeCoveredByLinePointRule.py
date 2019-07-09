# encoding: utf-8

import gvsig
import sys

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
    
    def check(self, taskStatus, report, feature1):
        try:
            store2 = self.getDataSet2().getFeatureStore()
            if self.expression == None:
                manager = ExpressionEvaluatorLocator.getManager()
                self.expression = manager.createExpression()
                self.expressionBuilder = manager.createExpressionBuilder()
                self.geomName = store2.getDefaultFeatureType().getDefaultGeometryAttributeName()
            point1 = feature1.getDefaultGeometry()
            tolerance1 = self.getTolerance()
            theDataSet2 = self.getDataSet2()
            if theDataSet2.getSpatialIndex() != None:
                if point1.getGeometryType().getName() == "Point2D":
                    buffer1 = point1.buffer(tolerance1)
                    contains = False
                    for featureReference in theDataSet2.query(buffer1):
                        feature2 = featureReference.getFeature()
                        line2 = feature2.getDefaultGeometry()
                        if line2.getGeometryType().getName() == "Line2D":
                            #numVertices = line2.getNumVertices()
                            if buffer1.intersects( line2 ):
                                contains = True
                                break
                        else:
                            if line2.getGeometryType().getName() == "MultiLineLine2D":
                                n2 = line2.getPrimitivesNumber()
                                for i in range(0, n2 + 1):
                                    curve2 = line2.getCurveAt(i)
                                    #numVertices = curve2.getNumVertices()
                                    if buffer1.intersects( curve2 ):
                                        contains = True
                                        break
                    if not contains:
                        report.addLine(self,
                                    self.getDataSet1(),
                                    self.getDataSet2(),
                                    point1,
                                    point1,
                                    feature1.getReference(), 
                                    None,
                                    False,
                                    "The point is not covered by line."
                        )
                else:
                    if point1.getGeometryType().getName() == "MultiPoint2D":
                        n1 = point1.getPrimitivesNumber()
                        for i in range(0, n1 + 1):
                            buffer1 = point1.getPointAt(i).buffer(tolerance1)
                            contains = False
                            for featureReference in theDataSet2.query(buffer1):
                                feature2 = featureReference.getFeature()
                                line2 = feature2.getDefaultGeometry()
                                if line2.getGeometryType().getName() == "Line2D":
                                    #numVertices = line2.getNumVertices()
                                    if buffer1.intersects( line2 ):
                                        contains = True
                                        break
                                else:
                                    if line2.getGeometryType().getName() == "MultiLineLine2D":
                                        n2 = line2.getPrimitivesNumber()
                                        for j in range(0, n2 + 1):
                                            curve2 = line2.getCurveAt(j)
                                            #numVertices = curve2.getNumVertices()
                                            if buffer1.intersects( curve2 ):
                                                contains = True
                                                break
                            if not contains:
                                report.addLine(self,
                                            self.getDataSet1(),
                                            self.getDataSet2(),
                                            point1.getPointAt(i),
                                            point1.getPointAt(i),
                                            feature1.getReference(), 
                                            None,
                                            False,
                                            "The multipoint is not covered by line."
                                )
        except:
            ex = sys.exc_info()[1]
            gvsig.logger("Can't execute rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass
