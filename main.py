from script import run, mesh_file
import sys

if len(sys.argv) == 2:
    if len(sys.argv[1].split('.')) == 1:
        print "Please enter a file with an extension"
    else:
        if sys.argv[1].split(".")[1] == 'mdl':
            run(sys.argv[1])
        elif sys.argv[1].split(".")[1] == 'obj':
            print "Mesh file"
            print "Meshing file..."
            mesh_file(sys.argv[1])
        else:
            print "Unrecognized file format"
        
elif len(sys.argv) == 1:
    run(raw_input("Please enter the filename of a file: \n"))
else:
    print "Too many arguments."
