import math
#import numpy
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#from matplotlib import style

G = 6.67408e-11
Msun = 1.989e30
GM = G*Msun
monthSecs = 2.628e6

fig = plt.figure()
ax1 = fig.add_subplot(111)


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

    def orbitSun(self, tstep):
        self.velx = self.velx -((GM*self.x)/(self.distance**3))*tstep
        self.vely = self.vely - ((GM*self.y) / (self.distance ** 3))*tstep
        self.x = self.x + self.velx * tstep
        self.y = self.y + self.vely * tstep


#Start with just earth and jupiter
def main():
    #Create our celestial bodies with initial conditions
    Earth = Body("Earth","Sun",0,1.496e11,5.972e24,30000,0)
    Jupiter = Body("Jupiter","Sun",0,816.62e9,1.8982e27,13070,0)
    tstep = int(float(input("Enter time step (months) : " ))*monthSecs)
    endtime = int(float(input("Enter end time (months) : "))*monthSecs)
    Exlist = [Earth.x]
    Eylist = [Earth.y]
    Jxlist = [Jupiter.x]
    Jylist = [Jupiter.y]
    for i in range(0,endtime,tstep):
        #Have Earth orbit the sun
        Earth.orbitSun(tstep)
        Jupiter.orbitSun(tstep)
        Exlist.append(Earth.x)
        Eylist.append(Earth.y)
        Jxlist.append(Jupiter.x)
        Jylist.append(Jupiter.y)
        ax1.scatter(Exlist,Eylist, label="Earth Orbit", color="g", marker="*")
        ax1.scatter(Jxlist,Jylist, label="Jupiter Orbit", color="r", marker="*")
        ax1.scatter(0,0, label="Fixed Sun", color="y")
        plt.pause(0.05)
    plt.show()


main()