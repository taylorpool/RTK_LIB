import matplotlib.pyplot as plt
import numpy as np
import unittest

def relative_vector_2d(delta_p1, i1, delta_p2, i2):
    
    rotate_right = np.array([ [0, -1], [1, 0]])
    j1 = rotate_right@i1
    j2 = rotate_right@i2
    alpha = np.arccos(np.dot(i1, i2))

    return delta_p2/np.sin(alpha)*j1 - delta_p1/np.sin(alpha)*j2

class TestRTK_2D(unittest.TestCase):

    def rtk_2d(self, true_relative_vector, i1, i2):
        i1 = i1/np.linalg.norm(i1)
        i2 = i2/np.linalg.norm(i2)
        pseudorange_1 = np.dot(true_relative_vector, i1)
        pseudorange_2 = np.dot(true_relative_vector, i2)
        relative_vector = relative_vector_2d(pseudorange_1, i1, pseudorange_2, i2)
        np.testing.assert_almost_equal(true_relative_vector, relative_vector)


    def test_1(self):
        true_relative_vector = np.array([2, 10])
        i1 = np.array([1, 2])
        i2 = np.array([-1, 1])
        self.rtk_2d(true_relative_vector, i1, i2)

    def test_2(self):
        true_relative_vector = np.array([5,0])
        i1 = np.array([1, 2])
        i2 = np.array([-1, 1])
        self.rtk_2d(true_relative_vector, i1, i2)

    def test_51_15(self):
        true_relative_vector = np.array([5,0])
        i1 = np.array([5, 1])
        i1 = i1/np.linalg.norm(i1)
        i2 = np.array([-5, 1])
        i2 = i2/np.linalg.norm(i2)
        pseudorange_1 = np.dot(true_relative_vector, i1)
        pseudorange_2 = np.dot(true_relative_vector, i2)
        relative_vector_1 = relative_vector_2d(pseudorange_1, i1, pseudorange_2, i2)
        np.testing.assert_almost_equal(true_relative_vector, relative_vector_1)

        i1_prime = np.array([1,5])
        i1_prime = i1_prime/np.linalg.norm(i1_prime)
        i2_prime = np.array([-1,5])
        i2_prime = i2_prime/np.linalg.norm(i2_prime)
        pseudorange_1_prime = np.dot(true_relative_vector, i1_prime)
        pseudorange_2_prime = np.dot(true_relative_vector, i2_prime)
        relative_vector_2 = relative_vector_2d(pseudorange_1_prime, i1_prime, pseudorange_2_prime, i2_prime)
        np.testing.assert_almost_equal(true_relative_vector, relative_vector_2)

    # @unittest.skip
    def test_through_angles(self):
        angles = np.linspace(0,np.pi,100)
        i = 1
        for magnitude in np.linspace(.1,10,20):
            for r_angle in angles:
                i1 = np.array([np.cos(r_angle*2), np.sin(r_angle*2)])
                i2 = np.array([np.cos(r_angle*10), np.sin(r_angle*10)])
                true_relative_vector = magnitude*np.array([np.cos(r_angle), np.sin(r_angle)])
                with self.subTest(i=i, i1 = i1, i2 = i2, r=true_relative_vector, dot=np.dot(i1,i2)):
                    if (i1==i2).all():
                        i2 = np.cos(r_angle*10+1), np.sin(r_angle*10+1)
                    self.rtk_2d(true_relative_vector, i1, i2)
                    i += 1

if __name__=='__main__':

    # unittest.main()

    fig = plt.figure()
    ax = fig.add_subplot()
    relative_vector = np.array([1.5, 2])
    origin = np.array([2, 1])
    ax.quiver(origin[0], origin[1], relative_vector[0], relative_vector[1], color='red', angles='xy', scale_units='xy', scale=1, label='Relative Vector')

    rotate_right = np.array([ [0, -1], [1, 0]])

    i1 = np.array([0.17364818, 0.98480775])
    i1 = i1/np.linalg.norm(i1)
    j1 = rotate_right@i1
    i2 = np.array([0.76604444, 0.64278761])
    i2 = i2/np.linalg.norm(i2)
    j2 = rotate_right@i2

    x = np.linspace(-2,6)
    ax.plot(x,i1[1]/i1[0]*x+origin[1]-i1[1]/i1[0]*origin[0], color='green', linestyle='dashed', label="Satellite 1 i")
    ax.plot(x, i1[1]/i1[0]*x+origin[1]+relative_vector[1]-i1[1]/i1[0]*(origin[0]+relative_vector[0]), color='green', linestyle = 'dashed')

    ax.plot(x, i2[1]/i2[0]*x+origin[1]-i2[1]/i2[0]*origin[0], color='blue', linestyle = 'dashed', label="Satellite 2 i")
    ax.plot(x, i2[1]/i2[0]*x+origin[1]+relative_vector[1]-i2[1]/i2[0]*(origin[0]+relative_vector[0]), color = 'blue', linestyle = 'dashed')

    ax.plot(x,j1[1]/j1[0]*x+origin[1]-j1[1]/j1[0]*origin[0], color='green', linestyle='dotted', label="Satellite 1 j")
    ax.plot(x, j1[1]/j1[0]*x+origin[1]+relative_vector[1]-j1[1]/j1[0]*(origin[0]+relative_vector[0]), color='green', linestyle='dotted')

    ax.plot(x,j2[1]/j2[0]*x+origin[1]-j2[1]/j2[0]*origin[0], color='blue', linestyle='dotted', label="Satellite 2 j")
    ax.plot(x, j2[1]/j2[0]*x+origin[1]+relative_vector[1]-j2[1]/j2[0]*(origin[0]+relative_vector[0]), color='blue', linestyle='dotted')

    ax.quiver(i1[0], i1[1], color='green', angles='xy', scale_units='xy', scale=1)
    ax.quiver(i2[0], i2[1], color='blue', angles='xy', scale_units='xy', scale=1)

    delta_p1 = np.dot(relative_vector, i1)
    ax.quiver(origin[0], origin[1], delta_p1*i1[0], delta_p1*i1[1], color='green', angles='xy', scale_units='xy', scale=1)

    delta_p2 = np.dot(relative_vector, i2)
    ax.quiver(origin[0], origin[1], delta_p2*i2[0], delta_p2*i2[1], color='blue', angles='xy', scale_units='xy', scale=1)

    alpha = np.arccos(np.dot(i1,i2))

    component_1 = delta_p1/np.sin(alpha)*j2
    ax.quiver(origin[0], origin[1], component_1[0], component_1[1], color='green', angles='xy', scale_units='xy', scale=1)

    component_2 = -delta_p2/np.sin(alpha)*j1
    ax.quiver(origin[0], origin[1], component_2[0], component_2[1], color='blue', angles='xy', scale_units='xy', scale=1)

    ax.quiver(component_1[0]+origin[0], component_1[1]+origin[1], component_2[0], component_2[1], color='black', angles='xy', scale_units='xy', scale=1)

    print(i2[1]/i2[0]-relative_vector[1]/relative_vector[0])
    ax.legend()
    ax.set_xlim(-20,20)
    ax.set_ylim(-20,20)

    ax.set_aspect('equal')
    plt.show()