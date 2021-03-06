"""========== script.py ==========

  This is the only file you need to modify in order
  to get a working mdl project (for now).

  my_main.c will serve as the interpreter for mdl.
  When an mdl script goes through a lexer and parser, 
  the resulting operations will be in the array op[].

  Your job is to go through each entry in op and perform
  the required action from the list below:

  frames: set num_frames for animation

  basename: set name for animation

  vary: manipluate knob values between two given frames
        over a specified interval

  set: set a knob to a given value
  
  setknobs: set all knobs to a given value

  push: push a new origin matrix onto the origin stack
  
  pop: remove the top matrix on the origin stack

  move/scale/rotate: create a transformation matrix 
                     based on the provided values, then 
		     multiply the current top of the
		     origins stack by it.

  box/sphere/torus: create a solid object based on the
                    provided values. Store that in a 
		    temporary matrix, multiply it by the
		    current top of the origins stack, then
		    call draw_polygons.

  line: create a line based on the provided values. Store 
        that in a temporary matrix, multiply it by the
	current top of the origins stack, then call draw_lines.

  save: call save_extension with the provided filename

  display: view the image live
  
  jdyrlandweaver
  ========================="""



import mdl
from display import *
from matrix import *
from draw import *


"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.

  jdyrlandweaver
  ==================== """
def first_pass( commands ):
    num_frames = None
    frameCheck = varyCheck = nameCheck = 0
    name = ''

    for command in commands:
        
        if command[0] == 'frames':
            num_frames = command[1]
            frameCheck = 1

        elif command[0] == 'vary':
            varyCheck = 1

        elif command[0] == 'basename':
            name = command[1]
            nameCheck = 1

    if varyCheck and not frameCheck:
        print 'Vary command found without setting number of frames!'
        exit()

    elif frameCheck and not nameCheck:
        print 'Animation code present but basename was not set. Using "frame" as basename.'
        name = 'frame'
    
    return (name, num_frames)
        

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands, num_frames ):

    frames = []
    for i in range( num_frames ):
        frames.append( {} )
        
    for command in commands:
        if command[0] == 'vary':
            knob = command[1]
            startFrame = command[2]
            endFrame = command[3]
            startValue = command[4]
            endValue = command[5]

            if (startFrame < 0) or (endFrame >= num_frames) or (endFrame < startFrame):
                print 'Invalid vary command for knob: ' + knob
                exit()
            
            if startValue < endValue:
                step = (float(endValue) - startValue) / (float(endFrame - startFrame))
            else:
                step = (float(endValue) - startValue) / (float(endFrame - startFrame))

            for f in range( num_frames ):

                frame = frames[f]
                
                if f < startFrame:
                    value = startValue

                elif f > endFrame:
                    value = endValue

                else:
                    if startValue < endValue:
                        value = (f - startFrame) * step + startValue
                    else:
                        value = (startFrame - f) * step
                
                frame[knob] = value
    return frames

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    (name, num_frames) = first_pass( commands )
    knobs = second_pass( commands, num_frames )

    light_sources = [] # Allows the user to enter light sources
    constants = [] # Allows the user to enter constants for lighting

        
    for f in range( num_frames ):

        stack = [ tmp ]
        screen = new_screen()    
        
        for command in commands:
            if command[0] == "pop":
                stack.pop()
                if not stack:
                    stack = [ tmp ]

            if command[0] == "push":
                stack.append( stack[-1][:] )

            if command[0] == "light":
                light_sources.append(list(command[1:])) # Add the light_sources from the user to the list

            if command[0] == "constants":
                constants = command[1:]

            if command[0] == "save":
                save_extension(screen, command[1])

            if command[0] == "display":
                display(screen)

            if command[0] == "sphere":
                m = []
                add_sphere(m, command[1], command[2], command[3], command[4], 5)
                matrix_mult(stack[-1], m)
                draw_polygons(m, screen, color, constants, light_sources)

            if command[0] == "torus":
                m = []
                add_torus(m, command[1], command[2], command[3], command[4], command[5], 5)
                matrix_mult(stack[-1], m)
                draw_polygons(m, screen, color, constants, light_sources)

            if command[0] == "box":                
                m = []
                add_box(m, *command[1:])
                matrix_mult(stack[-1], m)
                draw_polygons(m, screen, color, constants, light_sources)

            if command[0] == "line":
                m = []
                add_edge(m, *command[1:])
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )

            if command[0] == "bezier":
                m = []
                add_curve(m, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .05, 'bezier')
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )

            if command[0] == "hermite":
                m = []
                add_curve(m, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .05, 'hermite')
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )

            if command[0] == "circle":
                m = []
                add_circle(m, command[1], command[2], command[3], command[4], .05)
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )

            if command[0] == "move":                
                xval = command[1]
                yval = command[2]
                zval = command[3]

                if command[4]:
                    knob = knobs[f][command[4]]
                    xval*= knob
                    yval*= knob
                    zval*= knob
                    
                t = make_translate(xval, yval, zval)
                matrix_mult( stack[-1], t )
                stack[-1] = t

            if command[0] == "scale":
                xval = command[1]
                yval = command[2]
                zval = command[3]

                if command[4]:
                    knob = knobs[f][command[4]]
                    xval*= knob
                    yval*= knob
                    zval*= knob

                t = make_scale(xval, yval, zval)
                matrix_mult( stack[-1], t )
                stack[-1] = t

            if command[0] == "rotate":
                angle = command[2] * (math.pi / 180)

                if command[3]:
                    angle*= knobs[f][command[3]]

                if command[1] == 'x':
                    t = make_rotX( angle )
                elif command[1] == 'y':
                    t = make_rotY( angle )
                elif command[1] == 'z':
                    t = make_rotZ( angle )            
                    
                matrix_mult( stack[-1], t )
                stack[-1] = t
                
        if num_frames > 1:
            fname = 'anim/%s%03d.png' % (name, f)
            print 'Drawing frame: ' + fname
            save_extension(screen, fname)

def mesh_file(filename):
    color = [255, 255, 255]

    screen = new_screen()

    vertices = [['blah', 'blah', 'blah']]

    i = 0

    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0
    max_z = 0
    min_z = 0
    
    for line in open(filename).read().split('\n'):
        if not line == '' and line.split(' ')[0] == 'v':
            vertices.append([float(line.split(' ')[1]), float(line.split(' ')[2]), float(line.split(' ')[3])])

            if float(line.split(' ')[1]) > max_x:
                max_x = float(line.split(' ')[1])
            if float(line.split(' ')[1]) < min_x:
                min_x = float(line.split(' ')[1])
            if float(line.split(' ')[2]) > max_y:
                max_y = float(line.split(' ')[2])
            if float(line.split(' ')[2]) < min_y:
                min_y = float(line.split(' ')[2])
            if float(line.split(' ')[3]) > max_z:
                max_z = float(line.split(' ')[3])
            if float(line.split(' ')[3]) < min_z:
                min_z = float(line.split(' ')[3])
                
            i += 1

    print max_x
    print min_x
    print max_y
    print min_y
    
    x_scale_factor = XRES / (max_x - min_x + 2)
    y_scale_factor = YRES / (max_y - min_y + 2)
    
    print x_scale_factor
    print y_scale_factor
    
    scale_factor = 0.0
    if x_scale_factor < y_scale_factor:
        scale_factor = x_scale_factor
    else:
        scale_factor = y_scale_factor

    m = []
    for line in open(filename).read().split('\n'):
        if not line == '' and line.split(' ')[0] == 'f':
            add_polygon(m,
                        vertices[int(line.split(' ')[1])][0] * scale_factor,
                        vertices[int(line.split(' ')[1])][1] * scale_factor,
                        vertices[int(line.split(' ')[1])][2] * scale_factor,
                        vertices[int(line.split(' ')[2])][0] * scale_factor,
                        vertices[int(line.split(' ')[2])][1] * scale_factor,
                        vertices[int(line.split(' ')[2])][2] * scale_factor,
                        vertices[int(line.split(' ')[3])][0] * scale_factor,
                        vertices[int(line.split(' ')[3])][1] * scale_factor,
                        vertices[int(line.split(' ')[3])][2] * scale_factor)

    constants = [0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
    light_sources = [[10, 15, 1, 255, 0, 0]]


    tmp = new_matrix()
    ident( tmp )
    stack = [tmp]
    
    t = make_translate(XRES / 2.5, YRES / 2.5, 0)
    matrix_mult(stack[-1], t)
    stack[-1] = t

    matrix_mult(stack[-1], m)
    
    draw_polygons(m, screen, color, constants, light_sources)

    display(screen)
    save_ppm(screen, 'final_image.ppm')
    save_extension(screen, 'final_image.png')
            
                                 
                        
            
            
