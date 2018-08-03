import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patch
from matplotlib.collections import PatchCollection

# Define some useful physical constants
G = 6.67408e-11
Msun = 1.989e30
GM = G*Msun
month_secs = 2.628e6
astronomical_unit = 1.496e11

# Set up the plot
fig = plt.figure()
fig.suptitle("Solar System")
ax1 = fig.add_subplot(111)
line, = ax1.plot([], [], "--", markersize=7)
line2, = ax1.plot([], [], '--', markersize=7)
line3, = ax1.plot([], [], '--', markersize=7)
line4, = ax1.plot([], [], '--', markersize=7)
# Want lines in a list, later we can determine the number of planets and create lines list as required
lines = [line, line2, line3, line4]
sun_patch = [patch.Circle((0, 0), 1e10)]
sun_patch[0].set_facecolor('y')
sun_patch[0].set_edgecolor('y')
patch_collection = PatchCollection(sun_patch)
ax1.add_collection(patch_collection)
ax1.axis('equal')
ax1.set_xlim(-1.3e12, 1.3e12)
ax1.set_ylim(-1.3e12, 1.3e12)


# Class for objects that are affected by gravity, Sun, planets, moons and smaller
class Body:
    def __init__(self, name, parent, x, y, mass, velx, vely):
        self.name = name
        self.parent = parent
        self.x = x
        self.y = y
        self.distance = math.sqrt(x**2 + y**2)
        self.mass = mass
        self.velx = velx
        self.vely = vely
        self.historical_x = [x]
        self.historical_y = [y]

    def orbitSun(self, tstep):
        self.velx = self.velx - ((GM*self.x)/(self.distance**3)) * tstep
        self.vely = self.vely - ((GM*self.y) / (self.distance**3)) * tstep

    def orbitBody(self, partner, tstep):
        # Change the velocity of self and partner due to the effect of gravity between them
        r3 = math.sqrt((partner.x - self.x)**2+(partner.y - self.y)**2)**3
        # Change velocity of self
        self.velx = self.velx + ((G * partner.mass * (partner.x - self.x))/r3) * tstep
        self.vely = self.vely + ((G * partner.mass * (partner.y - self.y)) / r3) * tstep
        # Change velocity of partner
        partner.velx = partner.velx + ((G * self.mass * (self.x - partner.x)) / r3) * tstep
        partner.vely = partner.vely + ((G * self.mass * (self.y - partner.y)) / r3) * tstep


def gravityForces(bodies, tstep):
    # bodies is a list of Body objects (massive bodies)
    for i in range(0, len(bodies)-1):
        bodies[i].orbitSun(tstep)
        for partner in bodies[i+1:]:
            bodies[i].orbitBody(partner, tstep)
    bodies[-1].orbitSun(tstep)

    # Now update the position of each body
    for j in range(0, len(bodies)):
        bodies[j].x = bodies[j].x + bodies[j].velx * tstep
        bodies[j].y = bodies[j].y + bodies[j].vely * tstep
        bodies[j].historical_x.append(bodies[j].x)
        bodies[j].historical_y.append(bodies[j].y)


def animate(i, planet_list, tstep):
    # Plot the position of the planet
    for j in range(0, len(planet_list)):
        lines[j].set_data(planet_list[j].historical_x, planet_list[j].historical_y)

    gravityForces(planet_list, tstep)
    return lines


# Start with just earth and jupiter
def main():
    # Create our celestial bodies with initial conditions
    earth = Body("Earth", "Sun", 0, 1.496e11, 5.972e24, 30000, 0)
    jupiter = Body("Jupiter", "Sun", 0, 816.62e9, 1.8982e27, 13070, 0)
    mars = Body("Mars", "Sun", 2.492e11, 0, 6.39e23, 0, -22000)
    fake = Body("FakePlanet", "Sun", 9e11, 9e11, 2e26, 1000, -400)
    planet_list = [earth, jupiter, mars, fake]
    tstep = int(float(input("Enter time step (months) : "))*month_secs)
    ani = animation.FuncAnimation(fig, animate, fargs=(planet_list, tstep), interval=1, blit=True)
    plt.show()


main()
