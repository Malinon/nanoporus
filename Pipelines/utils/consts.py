SAMPLES_PER_TYPE = 75
EXCL_TOPO =  {15, 20, 21, 25, 26, 30, 35, 40, 45, 50, 65, 66, 70}
NUMBER_OF_OK_TOPO_SAMPLES = SAMPLES_PER_TYPE - len(EXCL_TOPO)
PERSISTENCE_IMAGE_RESOLUTION = (10,10)
from enum import Enum

class DataType(Enum):
    __order__ = 'WHOLE TOPO RAND'
    WHOLE="whole",
    TOPO="topo",
    RAND="rand",

class ConeZFiltParams:
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height
    def __str__(self):
        return "R"+str(self.radius)+"H"+str(self.height)