import unittest
import sys
import numpy as np
sys.path.append('../')

from weighted_filtration import get_weighted_pyramide_filtration

class WeightedPyramideTest(unittest.TestCase):
    def test_full_data(self):
        data = np.full((5,5,5), True)
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    self.assertEqual(1.0, get_weighted_pyramide_filtration((x,y,z), data, z_multiplier = 2,
                            xy_multiplier = 3, range_filt=2))

    def test_empty_data(self):
        data = np.full((5,5,5), False)
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    self.assertEqual(0, get_weighted_pyramide_filtration((x,y,z), data, z_multiplier = 2,
                            xy_multiplier = 3, range_filt=2))

    def test_in_the_middle(self):
        data = np.full((5,5,5), False)
        data[2, 2, 2] = True
        data[2, 2, 1] = True
        data[2, 2, 3] = True
        data[2, 3, 0] = True
        data[3, 2, 0] = True
        data[3, 1, 0] = True
        print(data)
        weight_normalization = 0
        z_multiplier = 4
        xy_multiplier = 5
        for z in range(-2,3):
            z_abs = abs(z)
            for x in range(-z_abs, z_abs + 1):
                for y in range(-z_abs, z_abs + 1):
                    weight_normalization += (z_multiplier ** z_abs) * (xy_multiplier ** (abs(x)+abs(y)))
        self.assertEqual(get_weighted_pyramide_filtration((2, 2, 2), data, z_multiplier = z_multiplier,
                            xy_multiplier = xy_multiplier, range_filt=2), (1 + 4 + 4 + 16 * 5 + 16 * 5 + 16 * 25) / weight_normalization )
    
    def test_in_corner(self):
        data = np.full((5,5,5), False)
        data[4, 4, 3] = True
        data[4, 3, 3] = True
        data[4, 3, 4] = True
        data[3, 3, 4] = True
        data[2, 3, 3] = True
        z_multiplier = 5
        xy_multiplier = 2
        weight_normalization = 0
        for z in range(-2, 1):
            for x in range(z, 1):
                for y in range(z, 1):
                    weight_normalization += (z_multiplier ** abs(z)) * (xy_multiplier ** (abs(x)+abs(y)))
        self.assertEqual(get_weighted_pyramide_filtration((4 ,4 ,4), data, z_multiplier =  z_multiplier,
                            xy_multiplier = xy_multiplier, range_filt=2), (z_multiplier * (1 + xy_multiplier)) / weight_normalization)

if __name__ == '__main__':
    unittest.main()