# boids

Boids are meant to simulate the behavior of flocks of birds or schools of fish through three rules:
- Separation: Maintain a minimum distance between boids.
- Alignment: Move each boid in the average direction of its neighboring boids.
- Cohesion: Move each boid towards the center of mass of its neighboring boids.

This is a simple implementation of this idea using Python and Matplotlub for the GUI. 
Credits for the explanation/discussion of this simulation go to Mahesh Venkitachalam in his
book, "Python Playground."

Controls:
- Left-click: Spawn a boid traveling in a random direction.
- Right-click: Deflect all boids away from the location of your click.

Click [here](http://imgur.com/JrjStfm) to see an example of the simulation in action.