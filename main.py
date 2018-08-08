import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define some useful physical constants
G = 6.67408e-11
M_SUN = 1.989e30
GM = G*M_SUN
MONTH_SECS = 2.628e6
ASTRONOMICAL_UNIT = 1.496e11

# Set up the plot
fig = plt.figure()
fig.suptitle("Solar System")
ax1 = fig.add_subplot(111)
ax1.axis('equal')
ax1.set_xlim(-1.3e12, 1.3e12)
ax1.set_ylim(-1.3e12, 1.3e12)
text_string = "0 mths."
time_text = ax1.text(0.05,0.9,text_string, transform=ax1.transAxes)


# Class for objects that are affected by gravity, Sun, planets, moons and smaller
class Body:
    def __init__(self, name, color, x, y, mass, velx, vely):
        self.name = name
        self.color = color
        self.x, self.y = x, y
        self.distance = math.sqrt(x**2 + y**2)
        self.mass = mass
        self.vel_x, self.vel_y = velx, vely
        self.historical_x, self.historical_y = [x], [y]
        self.year_complete = False

    def orbit_sun(self, tstep):
        self.vel_x = self.vel_x - ((GM*self.x)/(self.distance**3)) * tstep
        self.vel_y = self.vel_y - ((GM*self.y) / (self.distance**3)) * tstep

    def orbit_body(self, partner, tstep):
        # Change the velocity of self and partner due to the effect of gravity between them
        r3 = math.sqrt((partner.x - self.x)**2+(partner.y - self.y)**2)**3
        # Change velocity of self
        self.vel_x = self.vel_x + ((G * partner.mass * (partner.x - self.x))/r3) * tstep
        self.vel_y = self.vel_y + ((G * partner.mass * (partner.y - self.y)) / r3) * tstep
        # Change velocity of partner
        partner.vel_x = partner.vel_x + ((G * self.mass * (self.x - partner.x)) / r3) * tstep
        partner.vel_y = partner.vel_y + ((G * self.mass * (self.y - partner.y)) / r3) * tstep


def gravity_forces(bodies, tstep):
    # Have each planet interact with every other and the sun gravitationally
    for i in range(0, len(bodies)-1):
        bodies[i].orbit_sun(tstep)
        for partner in bodies[i+1:]:
            bodies[i].orbit_body(partner, tstep)
    bodies[-1].orbit_sun(tstep)

    # Now update the position of each body
    for j in range(0, len(bodies)):
        bodies[j].x = bodies[j].x + bodies[j].vel_x * tstep
        bodies[j].y = bodies[j].y + bodies[j].vel_y * tstep
        bodies[j].historical_x.append(bodies[j].x)
        bodies[j].historical_y.append(bodies[j].y)

        # Delete redundant historical data
        if len(bodies[j].historical_x) > 500:
            bodies[j].historical_x.pop(0)
            bodies[j].historical_y.pop(0)


def animate(i, planet_list, lines, tstep):
    # Update the elapsed time readout text
    month_step = tstep / MONTH_SECS
    if i * month_step > 24:
        time_text.set_text("%(current_time)i yrs." % {"current_time": int(i * month_step / 12)})
    else:
        time_text.set_text("%(current_time)g mths." % {"current_time": i * month_step})
    # Plot the positions of the planets
    for j in range(0, len(planet_list)):
        lines[2 * j].set_data(planet_list[j].x, planet_list[j].y)
        lines[(2 * j) + 1].set_data(planet_list[j].historical_x, planet_list[j].historical_y)
    # Apply the forces of gravity to each planet
    gravity_forces(planet_list, tstep)
    return lines + [time_text, ]


def main():
    # Create our celestial bodies with initial conditions
    earth = Body("Earth", "blue", 0, 1.496e11, 5.972e24, 30000, 0)
    jupiter = Body("Jupiter", "orange", 0, 816.62e9, 1.8982e27, 13070, 0)
    mars = Body("Mars", "red", 2.492e11, 0, 6.39e23, 0, -22000)
    fake = Body("FakePlanet", "pink", 9e11, 9e11, 2e26, 1000, -400)
    planet_list = [earth, jupiter, mars, fake]
    lines = []
    # Generate the line objects here for the planets and pass them to animate
    for i in range(0, len(planet_list)):
        planet_dot, = ax1.plot([], [], "o", markersize=5, color=planet_list[i].color)
        planet_line, = ax1.plot([], [], "-", markersize=1, color=planet_list[i].color)
        lines.append(planet_dot)
        lines.append(planet_line)

    # Add the sun last
    planet_dot, = ax1.plot(0, 0, "o", markersize=5, color="yellow")
    lines.append(planet_dot)

    tstep = 0.1 * MONTH_SECS
    ani = animation.FuncAnimation(fig, animate, fargs=(planet_list, lines, tstep), interval=1, blit=True)
    plt.show()


main()
