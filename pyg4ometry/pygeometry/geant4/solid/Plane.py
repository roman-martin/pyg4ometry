from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.geant4.Registry import registry as _registry
import math as _math

class Plane(_SolidBase) : # point on plane is on z-axis
    def __init__(self, name, normal, dist, zlength=10000):
        self.name   = name
        self.normal = _Vector(normal).unit()
        self.dist   = float(dist)
        self.pDz    = float(zlength)
        self.mesh   = None

    def __repr__(self):
        pass

    def pycsgmesh(self):
#        if self.mesh :
#            return self.mesh

        d = self.pDz
        c = _CSG.cube(radius=[10*d,10*d,d])

        dp = self.normal.dot(_Vector(0,0,1))

        if dp != 1 and dp != -1:
            cp = self.normal.cross(_Vector(0,0,1))
            an = _math.acos(dp)
            an = an/_math.pi*180.
            c.rotate(cp,an)

        c.translate(_Vector([0, 0, self.dist+d/dp]))

        self.mesh = c
        return self.mesh