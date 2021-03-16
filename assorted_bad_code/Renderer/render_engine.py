from turtle import *
from math import sqrt, sin, cos, radians
from importer import import_obj, import_mtl

#SETTINGS
size = 780
scale = 1
bgcolor(0,0,0)
obj_dist = 400
A1 = radians(2)
B1 = radians(6)
C1 = radians(4)
light_direction = [-1/3,1,3]
model = r"mario.obj"

#NORMALISING LIGHT DIRECTION
for i in range(0,len(light_direction)):
    light_direction[i] = light_direction[i]/(sqrt(light_direction[0]**2 + light_direction[1]**2 + light_direction[2]**2))

#SETUP
setup(size,size)
tracer(0,0)
pensize(2)
ht()
pu()
A = 0
B = 0
C = 0

#MESH CLASS
class Mesh:
    #CONSTRUCTOR
    def __init__(self, verts, faces, mtllib, materials):
        self.verts = verts
        self.faces = faces
        self.mtl_dict = import_mtl(mtllib)
        self.materials = materials
        self.v1 = verts.copy()
        self.normals = [[0 for i in range(3)] for j in range(len(faces))]
        self.centroids = [0 for i in range(len(faces))]
        self.Kd = []
        for face in range(len(self.faces)):
            key = list(self.materials)[len(self.materials)-1]
            for key in range(len(self.materials)):
                if face < list(self.materials)[key]:
                    current_mat = self.materials[list(self.materials)[key-1]]
                    break
            self.Kd.append(self.mtl_dict[current_mat]["Kd"])

    def centroid_sort(self, lst):
        return [i for (centroid,i) in sorted(zip(self.centroids,lst), key=lambda pair: pair[0])]
    
    #DRAW FUNCTION
    def draw(self, offset):
        for face in range(len(self.faces)):
            
            #APPLYING TRANSFORMATION MATRICES TO VERTICES 
            for v in self.faces[face]:
                self.v1[v] = [self.verts[v][0] * cosBcosC
                                        - self.verts[v][1] * cosBsinC
                                        + self.verts[v][2] * sinB,
                                       
                                        self.verts[v][0] * (sinAsinBcosC + cosAsinC)
                                        + self.verts[v][1] * (cosAcosC - sinAsinBsinC)
                                        - self.verts[v][2] * sinAcosB,
                                       
                                        self.verts[v][0] * (sinAsinC - cosAsinBcosC)
                                        + self.verts[v][1] * (cosAsinBsinC + sinAcosC)
                                        + self.verts[v][2] * cosAcosB]
                
            #FINDING CENTROIDS OF FACES
            self.centroids[face] = 0
            for vertex in self.faces[face]:
                self.centroids[face] += self.v1[vertex][2]/len(self.faces[face])

        #ORDERING FACES AND COLOURS ACCORDING TO Z COORDINATE OF CENTROIDS
        self.faces = self.centroid_sort(self.faces)
        self.Kd = self.centroid_sort(self.Kd)

        #CALCULATING NORMALS
        for face in range(len(self.faces)):
            a = [self.v1[self.faces[face][1]][i] - self.v1[self.faces[face][0]][i] for i in range(3)]
            b = [self.v1[self.faces[face][2]][i] - self.v1[self.faces[face][1]][i] for i in range(3)]
            
            self.normals[face] = [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

            #NORMALISING NORMALS
            normal_length = sqrt(sum([self.normals[face][i]**2 for i in range(3)]))
            if normal_length == 0:
                self.normals[face] = [0,0,0]
            else:
                self.normals[face] = [self.normals[face][i]/normal_length for i in range(3)]

        #RENDERING
        for face in range(len(self.faces)):
            
            #BACKFACE CULLING
            if self.normals[face][2] > 0:
                luminance = sum([self.normals[face][i] * light_direction[i] for i in range(3)])
                if luminance < 0:
                    luminance = 0
                if luminance > 1:
                    luminance = 1

                #SETTING COLOUR
                output = [self.Kd[face][i]*luminance for i in range(3)]
                fillcolor(output)
                pencolor(output)
                
                #DRAWING FACES
                begin_fill()
                for vertex in range(len(self.faces[face])+1):
                    vertex = vertex % len(self.faces[face])
                    z = self.v1[self.faces[face][vertex]][2]
                    goto(screen_dist*(self.v1[self.faces[face][vertex]][0] + offset[0])/(obj_dist - z),
                         screen_dist*(self.v1[self.faces[face][vertex]][1] + offset[1])/(obj_dist - z))
                    pd()
                end_fill()
                pu()

#IMPORTING FILE
file = import_obj(model)

#SETTING SCREEN DISTANCE
screen_dist = (scale * size * obj_dist)/(2 * file[4])

#CREATING OBJECT
mario = Mesh(file[0],file[1],file[2],file[3])

#MAIN LOOP
while True:

    #PRE-CALCULATING THINGS 
    clear()
    sinA = sin(A)
    sinB = sin(B)
    sinC = sin(C)
    cosA = cos(A)
    cosB = cos(B)
    cosC = cos(C)
   
    cosBcosC = cosB*cosC
    cosBsinC = cosB*sinC
    cosAsinC = cosA*sinC
    cosAcosC = cosA*cosC
    sinAcosB = sinA*cosB
    sinAsinC = sinA*sinC
    sinAcosC = sinA*cosC
    cosAcosB = cosA*cosB
   
    sinAsinBcosC = sinAcosC*sinB
    cosAsinBcosC = cosAcosC*sinB
    cosAsinBsinC = cosAsinC*sinB
    sinAsinBsinC = sinAsinC*sinB

    #DRAW FUNCTION
    mario.draw([0,0])
    update()

    #ROTATING
    A += A1
    B += B1
    C += C1

