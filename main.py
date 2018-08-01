import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Define some useful physical constants
G = 6.67408e-11
Msun = 1.989e30
GM = G*Msun
month_secs = 2.628e6

fig = plt.figure()
ax1 = fig.add_subplot(111)
line, = ax1.plot([],[], "-", markersize=7)
line2, = ax1.plot([],[],'--', markersize=7)
ax1.axis('equal')
ax1.set_xlim(-1.3e12, 1.3e12)
ax1.set_ylim(-1.3e12, 1.3e12)


#Class for objects that are affeted by gravity, Sun, planets, moons and smaller
class Body:
    def __init__(self, name, parent, x, y, mass, velx, vely):
        self.name = name
        self.parent = parent #What the body is orbiting (Sun or planet)
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
        self.x = self.x + self.velx * tstep
        self.y = self.y + self.vely * tstep
        self.historical_x.append(self.x)
        self.historical_y.append(self.y)
        return (self.x,self.y)

def animate(i, planet1,planet2, tstep):
    #Plot the position of the planet
    x1, y1 = planet1.historical_x, planet1.historical_y
    x2, y2 = planet2.historical_x, planet2.historical_y
    line.set_data(x1,y1)
    line2.set_data(x2,y2)
    planet1.orbitSun(tstep)
    planet2.orbitSun(tstep)
    return line, line2,


#Start with just earth and jupiter
def main():
    #Create our celestial bodies with initial conditions
    Earth = Body("Earth","Sun",0,1.496e11,5.972e24,30000,0)
    Jupiter = Body("Jupiter","Sun",0,816.62e9,1.8982e27,13070,0)
    tstep = int(float(input("Enter time step (months) : " ))*month_secs)
    ani = animation.FuncAnimation(fig,animate,fargs=(Earth,Jupiter,tstep),interval=10,blit=True)
    plt.show()

main()