from subprocess import Popen, PIPE
from os import remove

#constants
XRES = 500
YRES = 500
MAX_COLOR = 255
RED = 0
GREEN = 1
BLUE = 2

DEFAULT_COLOR = [0, 0, 0]

def new_screen( width = XRES, height = YRES ):
    screen = []
    for y in range( height ):
        row = []
        screen.append( row )
        for x in range( width ):
            screen[y].append( DEFAULT_COLOR[:] )
    return screen

# I am lazy, and don't want to edit the passing of everthing -- hence, it is here!!
z_buffer = [[-float('inf') for y in range(YRES)] for x in range(XRES)]
def clear_buff():
    global z_buffer
    
    z_buffer = [[-float('inf') for y in range(YRES)] for x in range(XRES)]

def plot( screen, color, x, y,z ):
    x = int(x)
    y = int(y)
    
    new_y = YRES - 1 - y
    
    if ( x >= 0 and x < XRES and new_y >= 0 and new_y < YRES ):
        if z > z_buffer[x][new_y]:
            z_buffer[x][new_y] = z
            
            screen[x][new_y] = color[:]

def clear_screen( screen ):
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            screen[x][y] = DEFAULT_COLOR[:]

def save_ppm( screen, fname ):
    f = open( fname, 'w' )
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range( len(screen) ):
        row = ''
        for x in range( len(screen[y]) ):
            pixel = screen[x][y]
            row+= str( pixel[ RED ] ) + ' '
            row+= str( pixel[ GREEN ] ) + ' '
            row+= str( pixel[ BLUE ] ) + ' '
        ppm+= row + '\n'
    f.write( ppm )
    f.close()

def save_extension( screen, fname ):
    ppm_name = fname[:fname.find('.')] + '.ppm'
    save_ppm( screen, ppm_name )
    p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

def display( screen ):
    ppm_name = 'pic.ppm'
    save_ppm( screen, ppm_name )
    Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )


