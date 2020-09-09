from matplotlib import pyplot as plt
import numpy as np

import unittest

def position_determiner(receiver_point, satellites, pseudoranges):

    H = np.hstack((-(satellites-receiver_point)/(np.linalg.norm(satellites-receiver_point, axis=1).reshape((4,1))), np.ones((4,1))))
    pseudoranges_0 = np.array([np.linalg.norm(receiver_point - satellite) for satellite in satellites])
    delta_x = np.linalg.inv(H)@(pseudoranges-pseudoranges_0).T
    return receiver_point + delta_x[:3], delta_x[3]

class TestGPS(unittest.TestCase):
    def test_1(self):
        sv_2 = np.array([7766188.44, -21960535.34, 12522838.56])
        sv_26 = np.array([-25922679.66, -6629461.28, 31864.37])
        sv_4 = np.array([-5743774.02, -25828319.92, 1692757.72])
        sv_7 = np.array([-2786005.69, -15900725.80, 21302003.49])
        p1 = 22228206.42
        p2 = 24096139.11
        p3 = 21729070.63
        p4 = 21259581.09
        satellites = np.array([sv_2, sv_26, sv_4, sv_7])
        pseudoranges = np.array([p1, p2, p3, p4])
        position = np.array([0,0,0])
        position, receiver_clock_bias = position_determiner(position, satellites, pseudoranges)
        np.testing.assert_almost_equal(position, np.array([-2977571.47597242, -5635278.15933945,  4304234.50558469]), 3)
        self.assertAlmostEqual(receiver_clock_bias, 1625239.8018165398)
        position, receiver_clock_bias = position_determiner(position, satellites, pseudoranges)
        np.testing.assert_almost_equal(position, np.array([-2451728.53419043, -4730878.46098024,  3573997.52045576]), 3)
        self.assertAlmostEqual(receiver_clock_bias, 314070.73267924064)

if __name__=='__main__':
    sv_2 = np.array([7766188.44, -21960535.34, 12522838.56])
    sv_26 = np.array([-25922679.66, -6629461.28, 31864.37])
    sv_4 = np.array([-5743774.02, -25828319.92, 1692757.72])
    sv_7 = np.array([-2786005.69, -15900725.80, 21302003.49])
    p1 = 22228206.42
    p2 = 24096139.11
    p3 = 21729070.63
    p4 = 21259581.09

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(sv_2, sv_26, sv_4, sv_7)
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    r = 6.371*10**6
    x = r*np.cos(u)*np.sin(v)
    y = r*np.sin(u)*np.sin(v)
    z = r*np.cos(v)
    ax.plot_wireframe(x, y, z,color='g')

    result = position_determiner(np.array([0,0,0]), np.array([sv_2, sv_26, sv_4, sv_7]), np.array([p1,p2,p3,p4]))
    print(result)
    result_2 = position_determiner(result[0], np.array([sv_2, sv_26, sv_4, sv_7]), np.array([p1,p2,p3,p4]))
    print(result_2)
    result_3 = position_determiner(result_2[0], np.array([sv_2, sv_26, sv_4, sv_7]), np.array([p1,p2,p3,p4]))
    print(result_3)
    # plt.show()
    unittest.main()