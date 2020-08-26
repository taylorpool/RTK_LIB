import unittest
import numpy as np

def get_unit_vectors(receiver_from_satellite):
    """Returns i along the path of the receiver from satellite,
    j right handed to it
    Ex: get_unit_vectors(np.array([1,0])) returns
    i: np.array([1,0])
    j: np.array([0,1])
    """
    theta = np.arccos(np.dot(receiver_from_satellite, np.array([1, 0])))
    R = np.array([ [np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)] ])
    return R@np.array([1,0]), R@np.array([0,1])

class UnitVectorsTest(unittest.TestCase):

    def test_north_of_satellite(self):
        satellite_location = np.array([-1,0])
        receiver_location = np.array([1,0])
        i, j = get_unit_vectors(receiver_location-satellite_location)
        self.assertTrue(np.equal(i, np.array([1,0])).all())
        self.assertTrue(np.equal(j, np.array([0,1])).all())

    def test_east_of_satellite(self):
        i, j = get_unit_vectors(np.array([0,1]))
        self.assertTrue(np.equal(i, np.array([0,1])).all())
        self.assertTrue(np.equal(j, np.array([1,0])).all())

if __name__ == '__main__':
    unittest.main()