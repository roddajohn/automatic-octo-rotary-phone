from display import *
from matrix import *
from gmath import *
from math import cos, sin, pi

MAX_STEPS = 100

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point( points, x0, y0, z0 )
    add_point( points, x1, y1, z1 )
    add_point( points, x2, y2, z2 )

def scanline_convert(screen, points, color):
    sorted_points = sorted(points, key = lambda x : x[1])
    x_top = int(sorted_points[2][0])
    x_middle = int(sorted_points[1][0])
    x_bottom = int(sorted_points[0][0])
    y_top = int(sorted_points[2][1])
    y_middle = int(sorted_points[1][1])
    y_bottom = int(sorted_points[0][1])
    z_bottom = int(sorted_points[0][2])
    z_middle = int(sorted_points[1][2])
    z_top = int(sorted_points[2][2])

    if y_top != y_bottom:
        delta_0 = float(x_top - x_bottom)/(y_top - y_bottom)
        delta_z_0 = float(z_top - z_bottom)/(y_top - y_bottom)
    else:
        delta_0 = 1.0
        delta_z_0 = 1.0
        
    y0 = y_bottom
    x0 = x_bottom
    x1 = x_bottom
    z0 = z_bottom
    z1 = z_bottom
    
    if y_middle == y_bottom:
        x1 = x_middle
        z1 = z_middle
        
    if y_middle != y_bottom:
        delta_1_bottom = float(x_middle - x_bottom)/(y_middle-y_bottom)
        delta_z_bottom = float(z_middle - z_bottom)/(y_middle-y_bottom)
        
    if y_top != y_middle:
        delta_1_top = float(x_top - x_middle)/(y_top-y_middle)
        delta_z_top = float(z_top - z_middle)/(y_top-y_middle)
        
    while(y0 < y_top):
        if y0 < y_middle:
            x1 += delta_1_bottom
            z1 += delta_z_bottom
        else:
            x1 += delta_1_top
            z1 += delta_z_top
            
        x0 += delta_0
        z0 += delta_z_0
        
        if x1 > x0:
            ztemp = (z1-z0) / (x1-x0)
            for xval in range(int(x0), int(x1)):
                plot(screen, color, xval, int(y0),z0+ ztemp * (xval - int(x0)))
        elif x1 < x0:
            ztemp = (z0-z1) / (x0-x1)
            for xval in range(int(x1), int(x0)):
                plot(screen, color, xval, int(y0), z1+ ztemp * (xval - int(x1)))
                
        y0 += 1
        
#    PREVIOUS VERSION -- DOESN'T WORK
#    increment = 0
#    while y_bottom + increment < y_top:
#        
#        d0 = float(x_top-x_bottom) / (y_top-y_bottom)
#        x_bottom0 = x_bottom + increment * d0
#        
#        if y_bottom + increment < y_middle:
#            d1 = float(x_middle-x_bottom)/(y_middle-y_bottom)
#            x_bottom1 = x_bottom + increment * d1
#            
#            draw_line(screen, x_bottom0, y_bottom + increment, x_bottom1, y_bottom + increment, color)
#            
#        else:
#            d1 = float(x_top-x_middle)/(y_top-y_middle)
#            x_middle1 = x_middle + (increment-y_middle + y_bottom) * d1
#            
#            draw_line(screen, x_bottom0, y_bottom + increment, x_middle1, y_bottom + increment, color)
#            
#        increment += 1

def sort_points( points, p ): # I used to use this function, then I found a better way (see above)
    x_middle = 0
    y_middle = 0
    x_top = 0
    y_top = 0
    x_bottom = 0
    y_bottom = 0
    
    if points[p][1] >= points[p + 1][1] and points[p][1] >= points[p + 2][1]:
        x_top = points[p][0]
        y_top = points[p][1]
        
        if points[p + 1][1] >= points[p + 2][1]:
            x_middle = points[p + 1][0]
            y_middle = points[p + 1][1]
                    
            x_bottom = points[p + 2][0]
            y_bottom = points[p + 2][1]

        else:
            x_bottom = points[p + 1][0]
            y_bottom = points[p + 1][1]
            
            x_middle = points[p + 2][0]
            y_middle = points[p + 2][1]

    elif points[p + 1][1] >= points[p][1] and points[p + 1][1] >= points[p + 2][1]:
        x_top = points[p + 1][0]
        y_top = points[p + 1][1]
        
        if points[p][1] >= points[p + 2][1]:
            x_middle = points[p][0]
            y_middle = points[p][1]
            
            x_bottom = points[p + 2][0]
            y_bottom = points[p + 2][1]
            
        else:
            x_bottom = points[p][0]
            y_bottom = points[p][1]
            
            x_middle = points[p + 2][0]
            y_middle = points[p + 2][1]

    elif points[p + 2][1] >= points[p][1] and points[p + 2][1] >= points[p + 1][1]:
        x_top = points[p + 2][0]
        y_top = points[p + 2][1]
        
        if points[p][1] >= points[p + 1][1]:
            x_middle = points[p][0]
            y_middle = points[p][1]
            
            x_bottom = points[p + 1][0]
            y_bottom = points[p + 1][1]
            
        else:
            x_bottom = points[p][0]
            y_bottom = points[p][1]
                    
            x_middle = points[p + 1][0]
            y_middle = points[p + 1][1]

    return [x_middle, y_middle, x_bottom, y_bottom, x_top, y_top]

            
    
def draw_polygons( points, screen, color, constants, light_sources ):

    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return

    p = 0

    view = [0, 0, 1] # view vector
    
    while p < len( points ) - 2:        # middle bottom top
        # Call the scanline helper function on the polygon of the three vertices that we are currently dealing with.
        
        if calculate_dot( points, p ) < 0:
            color = get_color(color, light_sources, constants, normalize(calculate_normal(
                points[p + 1][0] - points[p][0],
                points[p + 1][1] - points[p][1],
                points[p + 1][2] - points[p][2],
                points[p + 2][0] - points[p][0],
                points[p + 2][1] - points[p][1],
                points[p + 2][2] - points[p][2])), view)

            scanline_convert(screen,
                             points[p : p + 3],
                             color)
            
#            draw_line( screen, points[p][0], points[p][1],
#                       points[p+1][0], points[p+1][1], color )
#            draw_line( screen, points[p+1][0], points[p+1][1],
#                       points[p+2][0], points[p+2][1], color )
#            draw_line( screen, points[p+2][0], points[p+2][1],
#                       points[p][0], points[p][1], color )

        p += 3



def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon( points, 
                 x, y, z, 
                 x, y1, z,
                 x1, y1, z)
    add_polygon( points, 
                 x1, y1, z, 
                 x1, y, z,
                 x, y, z)
    #back
    add_polygon( points, 
                 x1, y, z1, 
                 x1, y1, z1,
                 x, y1, z1)
    add_polygon( points, 
                 x, y1, z1, 
                 x, y, z1,
                 x1, y, z1)
    #top
    add_polygon( points, 
                 x, y, z1, 
                 x, y, z,
                 x1, y, z)
    add_polygon( points, 
                 x1, y, z, 
                 x1, y, z1,
                 x, y, z1)
    #bottom
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y1, z,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y1, z1,
	         x1, y1, z1)
    #right side
    add_polygon( points, 
                 x1, y, z, 
                 x1, y1, z,
                 x1, y1, z1)
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y, z1,
                 x1, y, z)
    #left side
    add_polygon( points, 
                 x, y, z1, 
                 x, y1, z1,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y, z,
                 x, y, z1) 


def add_sphere( points, cx, cy, cz, r, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_sphere( temp, cx, cy, cz, r, step )
    num_points = len( temp )

    lat = 0
    lat_stop = num_steps
    longt = 0
    longt_stop = num_steps

    num_steps += 1

    while lat < lat_stop:
        longt = 0
        while longt < longt_stop:
            
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]
            
            if longt != longt_stop - 1:
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]
            else:
                px2 = temp[ (index + 1) % num_points ][0]
                py2 = temp[ (index + 1) % num_points ][1]
                pz2 = temp[ (index + 1) % num_points ][2]
                
            px3 = temp[ index + 1 ][0]
            py3 = temp[ index + 1 ][1]
            pz3 = temp[ index + 1 ][2]
      
            if longt != 0:
                add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 )

            if longt != longt_stop - 1:
                add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 )
            
            longt+= 1
        lat+= 1

def generate_sphere( points, cx, cy, cz, r, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle <= circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = r * cos( pi * circ ) + cx
            y = r * sin( pi * circ ) * cos( 2 * pi * rot ) + cy
            z = r * sin( pi * circ ) * sin( 2 * pi * rot ) + cz
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step

def add_torus( points, cx, cy, cz, r0, r1, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_torus( temp, cx, cy, cz, r0, r1, step )
    num_points = len(temp)

    lat = 0
    lat_stop = num_steps
    longt_stop = num_steps
    
    while lat < lat_stop:
        longt = 0

        while longt < longt_stop:
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]

            if longt != num_steps - 1:            
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]

                px3 = temp[ (index + 1) % num_points ][0]
                py3 = temp[ (index + 1) % num_points ][1]
                pz3 = temp[ (index + 1) % num_points ][2]
            else:
                px2 = temp[ ((lat + 1) * num_steps) % num_points ][0]
                py2 = temp[ ((lat + 1) * num_steps) % num_points ][1]
                pz2 = temp[ ((lat + 1) * num_steps) % num_points ][2]

                px3 = temp[ (lat * num_steps) % num_points ][0]
                py3 = temp[ (lat * num_steps) % num_points ][1]
                pz3 = temp[ (lat * num_steps) % num_points ][2]


            add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 );
            add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 );        
            
            longt+= 1
        lat+= 1


def generate_torus( points, cx, cy, cz, r0, r1, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = (cos( 2 * pi * rot ) *
                 (r0 * cos( 2 * pi * circ) + r1 ) + cx)
            y = r0 * sin(2 * pi * circ) + cy
            z = (sin( 2 * pi * rot ) *
                 (r0 * cos(2 * pi * circ) + r1))
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    t = step
    while t<= 1:
        
        x = r * cos( 2 * pi * t ) + cx
        y = r * sin( 2 * pi * t ) + cy

        add_edge( points, x0, y0, cz, x, y, cz )
        x0 = x
        y0 = y
        t+= step
    add_edge( points, x0, y0, cz, cx + r, cy, cz )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    xcoefs = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    ycoefs = generate_curve_coefs( y0, y1, y2, y3, curve_type )
        
    t =  step
    while t <= 1:
        
        x = xcoefs[0][0] * t * t * t + xcoefs[0][1] * t * t + xcoefs[0][2] * t + xcoefs[0][3]
        y = ycoefs[0][0] * t * t * t + ycoefs[0][1] * t * t + ycoefs[0][2] * t + ycoefs[0][3]

        add_edge( points, x0, y0, 0, x, y, 0 )
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1],
                   matrix[p+1][0], matrix[p+1][1], color )
        p+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )

def draw_line( screen, x0, y0, x1, y1, color ):
    dx = x1 - x0
    dy = y1 - y0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    
    if dx == 0:
        y = y0
        while y <= y1:
            plot(screen, color,  x0, y)
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            plot(screen, color, x, y0)
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx

