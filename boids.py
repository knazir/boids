import argparse
import math
import matplotlib.pyplot as plot
import matplotlib.animation as animation
import numpy

from scipy.spatial.distance import squareform, pdist, cdist
from numpy.linalg import norm

# # # # # # #
# Constants #
# # # # # # #

# Graphics
WIDTH = 640
HEIGHT = 480
POINT_SIZE = 10
BEAK_SIZE = 4
ANIMATION_INTERVAL = 25

# Simulation
DEFAULT_BOIDS = 100
MINIMUM_DISTANCE = 25.0
DISTANCE_THRESHOLD = 50.0
MAX_RULE_VELOCITY = 0.03
MAX_VELOCITY = 2.0
SCATTERING_VELOCITY_FACTOR = 0.1


# # # # # # # #
# Boids Class #
# # # # # # # #

class Boids:
    def __init__(self, n):
        # Initialize other fields
        self.n = n
        self.distance_matrix = None

        # Compute initial position and velocity
        self.position = [WIDTH/2.0, HEIGHT/2.0] + (10 * numpy.random.rand(2 * self.n)).reshape(self.n, 2)
        angles = 2 * math.pi * numpy.random.rand(self.n)
        self.velocity = numpy.array(list(zip(numpy.sin(angles), numpy.cos(angles))))

    # Animate single frame for boids
    def tick(self, frame_number, points, beak):
        # Compute pairwise distances
        self.distance_matrix = squareform(pdist(self.position))

        # Apply rules
        self.velocity += self.apply_rules()
        self.limit(self.velocity, MAX_VELOCITY)
        self.position += self.velocity
        self.apply_boundary_conditions()

        # Update data
        points.set_data(self.position.reshape(2 * self.n)[::2],
                        self.position.reshape(2 * self.n)[1::2])
        vector = self.position + 10 * self.velocity/MAX_VELOCITY
        beak.set_data(vector.reshape(2 * self.n)[::2],
                      vector.reshape(2 * self.n)[1::2])

    # Limit the magnitude of the 2D vector
    def limit_vector(self, vector, max_value):
        magnitude = norm(vector)
        if magnitude > max_value:
            for i in range(0, 2):
                vector[i] = vector[i] * max_value/magnitude

    # Limit the magnitude of 2D vectors in array x to max_value
    def limit(self, x, max_value):
        for vector in x:
            self.limit_vector(vector, max_value)

    def apply_boundary_conditions(self):
        delta_r = 2.0
        for coord in self.position:
            if coord[0] > WIDTH + delta_r:
                coord[0] = -delta_r
            if coord[0] < -delta_r:
                coord[0] = WIDTH + delta_r
            if coord[1] > HEIGHT + delta_r:
                coord[1] = -delta_r
            if coord[1] < -delta_r:
                coord[1] = HEIGHT + delta_r

    def apply_rules(self):
        velocity = 0

        # Apply separation
        distance = self.distance_matrix < MINIMUM_DISTANCE
        separation_velocity = self.position * distance.sum(axis=1).reshape(self.n, 1) - distance.dot(self.position)
        self.limit(separation_velocity, MAX_RULE_VELOCITY)
        velocity += separation_velocity

        # Distance threshold for alignment
        distance = self.distance_matrix < DISTANCE_THRESHOLD

        # Apply alignment
        alignment_velocity = distance.dot(self.velocity)
        self.limit(alignment_velocity, MAX_RULE_VELOCITY)
        velocity += alignment_velocity

        # Apply cohesion
        cohesion_velocity = distance.dot(self.position) - self.position
        self.limit(cohesion_velocity, MAX_RULE_VELOCITY)
        velocity += cohesion_velocity

        return velocity

    # Event handler for matplotlib
    def button_press(self, event):
        # Left click: add a boid
        if event.button is 1:
            self.position = numpy.concatenate((self.position, numpy.array([[event.xdata, event.ydata]])), axis=0)

            # Generate random velocity
            angles = 2 * math.pi * numpy.random.rand(1)
            vector = numpy.array(list(zip(numpy.sin(angles), numpy.cos(angles))))
            self.velocity = numpy.concatenate((self.velocity, vector), axis=0)
            self.n += 1

        # Right click: scatter boids
        elif event.button is 3:
            # Generate scattering velocity
            self.velocity += SCATTERING_VELOCITY_FACTOR * (self.position - numpy.array([[event.xdata, event.ydata]]))


# # # # # # # # # # #
# Simulation Driver #
# # # # # # # # # # #

def parse_args():
    parser = argparse.ArgumentParser(description="A simulation of Craig Reynold's Boids")
    parser.add_argument('--num-boids', dest='n', required=False)
    return parser.parse_args()


def tick(frame_number, points, beak, boids):
    boids.tick(frame_number, points, beak)
    return points, beak


def main():
    args = parse_args()

    # Set up simulation
    n = DEFAULT_BOIDS
    if args.n:
        n = int(args.n)
    boids = Boids(n)

    # Set up plot
    figure = plot.figure()
    axes = plot.axes(xlim=(0, WIDTH), ylim=(0, HEIGHT))

    points, = axes.plot([], [], markersize=POINT_SIZE, c='k', marker='o', ls='None')
    beak, = axes.plot([], [], markersize=BEAK_SIZE, c='r', marker='o', ls='None')
    figure_animation = animation.FuncAnimation(figure, tick, fargs=(points, beak, boids), interval=ANIMATION_INTERVAL)

    # Add event handler
    click = figure.canvas.mpl_connect('button_press_event', boids.button_press)

    plot.show()


# Credits to Mahesh Venkitachalam for his discussion of the algorithm in Python Playground
if __name__ == '__main__':
    main()