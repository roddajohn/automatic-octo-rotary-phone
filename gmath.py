from math import sqrt

def calculate_normal( ax, ay, az, bx, by, bz ):
    normal = [0,0,0]
    normal[0] = ay * bz - az * by
    normal[1] = az * bx - ax * bz
    normal[2] = ax * by - ay * bx
    return normal

def calculate_dot( points, i ):
    #get as and bs to calculate the normal
    ax = points[i + 1][0] - points[ i ][0]
    ay = points[i + 1][1] - points[ i ][1]
    az = points[i + 1][2] - points[ i ][2]

    bx = points[i + 2][0] - points[ i ][0]
    by = points[i + 2][1] - points[ i ][1]
    bz = points[i + 2][2] - points[ i ][2]

    normal = calculate_normal( ax, ay, az, bx, by, bz )

    #set up the view vector values
    vx = 0
    vy = 0
    vz = -1
    
    #calculate the dot product
    dot = normal[0] * vx + normal[1] * vy + normal[2] * vz
    
    return dot

def normalize(v):
    magnitude = sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)

    to_return = [0, 0, 0]
    for x in range(3):
        if magnitude != 0:
            to_return[x] = v[x] / magnitude
        else:
            to_return[x] = v[x]
    return to_return

def sub_vectors(v0, v1):
    to_return = v0
    for x in range(len(v0)):
        to_return[x] = v0[x]-v1[x]
    return to_return
    
def scalar_product(v, s):
    for x in range(3):
        v[x] *= s
    return v

def dot_product(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]

def get_color(color, light_sources, constants, normal, view):
    ambient = [0, 0, 0]
    diffuse = [0, 0, 0]
    specular = [0, 0, 0]

#    print color
#    print constants
    
    for x in range(3):
        ambient[x] = color[x] * constants[x]
        
    for source in light_sources:
        s = source[0:3]
        
        diffuse_light = [0, 0, 0]
        specular_light = [0, 0, 0]
    
        for x in range(3):
            diffuse_light[x] = source[x+3] * constants[x+3] * dot_product(normalize(normal), normalize(s))
            
            temp = dot_product(normalize(s), normalize(normal))
            temp = scalar_product(normalize(normal), temp)
            temp = sub_vectors(temp, normalize(s))
            temp = scalar_product(temp, 2)
            temp = dot_product(temp, view)
            angle = pow(temp,2)
            
            specular_light[x] = source[x+3] * constants[x+6] * angle
            specular_light[x] == 0
            
            if diffuse_light[x] > 0:
                diffuse[x] += diffuse_light[x]
                
            if specular_light[x] > 0:
                specular[x] += specular_light[x]
                    
    color_to_return = [0, 0, 0]
                    
    for x in range(3):
        c = int(ambient[x]) + int(diffuse[x]) + int(specular[x])
                        
        if c < 0:
            color_to_return[x] = c
        elif c > 255:
            color_to_return[x] = 255
        else:
            color_to_return[x] = c
            
    return color_to_return
                        
