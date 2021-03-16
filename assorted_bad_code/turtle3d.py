##this is probably not very good but wow look it's one of the first programs i was actually kind of proud of

from turtle import *
from math import *
from time import *

tracer(0)
colormode(1)
bgcolor(0,0,0)
pencolor(1, 1, 1)

scale = 70

setup(1400,900)
ht()

circle_res = 20

cone_lat_res = 10
cone_long_res = 16

cylinder_lat_res = 5
cylinder_long_res = 16

sphere_lat_res = 16
sphere_long_res = 16

torus_lat_res = 24
torus_long_res = 50
torus_minor_rad = 0.5

start_rot = 0.5
end_rot = 5*pi
rot_steps = 8

width_scale = 0.35 * 1200 / rot_steps
if width_scale < scale:
    scale = width_scale

pu()

for step in range(0, rot_steps):
    rot = start_rot + step*end_rot/rot_steps
    x_pos = step*1200/(rot_steps) - 600
    
    #CONE
    #Lat
    for line in range(-cone_lat_res, cone_lat_res+1):
        z = line/cone_lat_res
        for t in range(0,circle_res+1):
            t1 = 2*pi*t/circle_res
            x = z * cos(t1)
            y = z * (sin(rot) * sin(t1) + cos(rot))
            goto(scale*x + x_pos,scale*y + 281.25)
            pd()
        pu()
    #Long
    for line in range(0, cone_long_res+1):
        line1 = 2*pi*line/cone_long_res
        for t in range(-1,2):
            x = t * cos(line1)
            y = t * (sin(rot) * sin(line1) + cos(rot))
            goto(scale*x + x_pos,scale*y + 281.25)
            pd()
        pu()

    #SPHERE
    #Lat
    for line in range(0, sphere_lat_res//2 +1):
        line1 = 2*pi*line/sphere_lat_res
        for t in range(0,circle_res+1):
            t1 = 2*pi*t/circle_res
            x = sin(line1) * cos(t1)
            y = sin(rot) * sin(line1) * sin(t1) + cos(line1) * cos(rot)
            goto(scale*x + x_pos,scale*y + 93.75)
            pd()
        pu()
    #Long
    for line in range(0, sphere_long_res//2 +1):
        line1 = 2*pi*line/sphere_long_res
        for t in range(0, circle_res+1):
            t1 = 2*pi*t/circle_res
            x = sin(t1) * cos(line1)
            y = cos(t1) * cos(rot) + sin(t1) * sin(line1) * sin(rot)
            goto(scale*x + x_pos,scale*y + 93.75)
            pd()
        pu()

    #TORUS
    #Lat
    for line in range(0,torus_lat_res +1):
        line1 = 2*pi*line/torus_lat_res
        for t in range(0,circle_res+1):
            t1 = 2*pi*t/circle_res
            x = cos(t1) * (torus_minor_rad*cos(line1)+1)
            y = sin(t1) * sin(rot) * (torus_minor_rad*cos(line1)+1) + torus_minor_rad * cos(rot) * sin(line1)
            goto((2/3)*scale*x + x_pos,(2/3)*scale*y - 93.75)
            pd()
        pu()
    #Long
    for line in range(0,torus_long_res+1):
        line1 = 2*pi*line/torus_long_res
        for t in range(0,circle_res+1):
            t1 = 2*pi*t/circle_res
            x = torus_minor_rad * cos(t1) * cos(line1) + cos(line1)
            y = torus_minor_rad * (cos(t1) * sin(line1) * sin(rot) + sin(t1) * cos(rot)) + sin(line1) * sin(rot)
            goto((2/3)*scale*x + x_pos,(2/3)*scale*y - 93.75)
            pd()
        pu()

    #CYLINDER
    #Lat
    for line in range(-cylinder_lat_res, cylinder_lat_res+1):
        z = line/cylinder_lat_res
        for t in range(0,circle_res+1):
            t1 = 2*pi*t/circle_res
            x = cos(t1)
            y = sin(rot) * sin(t1) + z * cos(rot)
            goto(scale*x + x_pos,scale*y - 281.25)
            pd()
        pu()
    #Long
    for line in range(0, cylinder_long_res+1):
        line1 = 2*pi*line/cylinder_long_res
        for t in range(0,2):
            x = cos(line1)
            y = sin(rot) * sin(line1) + (t*2-1)*cos(rot)
            goto(scale*x + x_pos,scale*y - 281.25)
            pd()
        pu()
    

update()

