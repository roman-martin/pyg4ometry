from SolidBase import SolidBase as _SolidBase

from Tubs import Tubs as _Tubs
from Plane import Plane as _Plane

import numpy as _np
import logging as _log

class CutTubs(_SolidBase):
    """
    Constructs a cylindrical section with end face cuts. Note pLowNorm and pHighNorm can be lists of floats, Constants, Quantities or Variables.

    :param name: of solid for registry
    :type name: str
    :param pRMin: Inner radius
    :type pRMin: float, Constant, Quantity, Variable
    :param pRMax: Outer radius
    :type pRMax: float, Constant, Quantity, Variable
    :param pDz: length along z
    :type pDz: float, Constant, Quantity, Variable
    :param pSPhi: starting phi angle
    :type pSPhi: float, Constant, Quantity, Variable
    :param pDPhi: angle of segment
    :type pDPhi: float, Constant, Quantity, Variable
    :param pLowNorm: normal vector of the cut plane at -pDz/2
    :type pLowNorm: list 
    :param pHighNorm: normal vector of the cut plane at +pDz/2
    :type pHighNorm: list 
    """
    def __init__(self, name, pRMin, pRMax, pDz, pSPhi, pDPhi,
                 pLowNorm, pHighNorm, registry, lunit="mm",
                 aunit="rad", nslice=16, addRegistry = True):

        self.type      = 'CutTubs'
        self.name      = name
        self.pRMin     = pRMin
        self.pRMax     = pRMax
        self.pDz       = pDz
        self.pSPhi     = pSPhi
        self.pDPhi     = pDPhi
        self.pLowNorm  = pLowNorm
        self.pHighNorm = pHighNorm

        self.nslice    = nslice
        self.lunit     = lunit
        self.aunit     = aunit
        self.dependents = []

        self.varNames = ["pRMin", "pRMax", "pDz","pSPhi","pDPhi","pLowNorm","pHighNorm"]

        if addRegistry :
            registry.addSolid(self)

        self.registry = registry

    def __repr__(self):
        # Low norm and high norm exlcluded as they are lists
        return "Cut tubs : {} {} {} {} {} {}".format(self.name, self.pRMin, self.pRMax,
                                                        self.pDz, self.pSPhi, self.pDPhi)
    def pycsgmesh(self):

        _log.info('cuttubs.pycsgmesh> antlr')

        import pyg4ometry.gdml.Units as _Units #TODO move circular import
        luval = _Units.unit(self.lunit)
        auval = _Units.unit(self.aunit)

        pRMin     = self.evaluateParameter(self.pRMin)*luval
        pRMax     = self.evaluateParameter(self.pRMax)*luval
        pDz       = self.evaluateParameter(self.pDz)*luval/2.
        pSPhi     = self.evaluateParameter(self.pSPhi)*auval
        pDPhi     = self.evaluateParameter(self.pDPhi)*auval

        pHighNorm = [val*luval for val in self.evaluateParameter(self.pHighNorm)]
        pLowNorm = [val*luval for val in self.evaluateParameter(self.pLowNorm)]

        _log.info('cuttubs.pycsgmesh> mesh')
        mesh = _Tubs("tubs_temp", pRMin, pRMax, 2 * pDz, pSPhi, pDPhi, # Units are already rendered
                     registry=self.registry, nslice=self.nslice, addRegistry=False).pycsgmesh()

        if pLowNorm != [0,0,-1] or pHighNorm != [0,0,1]:
                
            zlength = 3 * pDz  # make the dimensions of the semi-infinite plane large enough
            if pHighNorm != [0,0,1]:
                pHigh = _Plane("pHigh_temp", pHighNorm, pDz, zlength).pycsgmesh()
                mesh = mesh.subtract(pHigh)
            if pLowNorm != [0,0,-1]:
                pLow  = _Plane("pLow_temp", pLowNorm, -pDz, zlength).pycsgmesh()
                mesh = mesh.subtract(pLow)
                
            return mesh
        else : 
            return mesh
