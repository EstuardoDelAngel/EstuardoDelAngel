#IMPORT .OBJ FILES
def import_obj(name):
    verts = []
    materials = {}
    faces = []
    
    #FINDS BIGGEST/SMALLEST VALUES FOR EACH AXIS
    max_values = [[0 for i in range(3)] for i in range(2)]
    
    obj = open(name,"r").readlines()
    for line in [i.split() for i in obj]:
        try:
            if line[0] == "v":
                
                #READS VERTEX COORDINATES
                vert = [float(line[i]) for i in range(1,len(line))]
                verts.append(vert)
                
                #ADDS TO MAX_VALUES
                max_values = [[max(vert[i],max_values[0][i]) for i in range(3)],
                               [min(vert[i],max_values[1][i]) for i in range(3)]]
                
            #READS FACE VERTICES#READS FACE VERTICES
            if line[0] == "f":
                faces.append([int(line[i].split("/")[0])-1 for i in range(1,len(line))])

            #READS MATERIAL LIBRARY
            if line[0] == "mtllib":
                mtllib = line[1]

            #READS MATERIAL
            if line[0] == "usemtl":
                materials[len(faces)] = line[1]

        #EXCEPTION FOR IF LINE IS EMPTY
        except:
            pass
        
    #FINDS AVERAGE OF MAX_VALUES
    average = [(max_values[0][i] + max_values[1][i])/2 for i in range(3)]

    #MOVES VERTICES TO BE CENTRED ON THE AVERAGE
    verts = [[i[j] - average[j] for j in range(3)] for i in verts]
    return [verts, faces, mtllib, materials,
            max([max([abs(j) for j in i]) for i in max_values])]

#IMPORT .MTL FILES
def import_mtl(name):

    #OPENS .MTL AND SPLITS BY MATERIAL
    mtl = open(name,"r").read().split("newmtl ")
    mtl_dict = {}
    for i in range(1,len(mtl)):
        
        #SPLITS LINE INTO DIFFERENT PARTS
        material = mtl[i].split("\n")

        #CREATES KEY FOR MATERIAL NAME
        mtl_dict[material[0]] = {}

        for line in [material[i].split() for i in range(1,len(material))]:
            try:
                
                #READS DIFFUSE COLOUR
                if line[0] == "Kd":
                    mtl_dict[material[0]]["Kd"] = [float(i) for i in line[1:]]

            #EXCEPTION IF LINE IS EMPTY
            except:
                pass
    return mtl_dict


