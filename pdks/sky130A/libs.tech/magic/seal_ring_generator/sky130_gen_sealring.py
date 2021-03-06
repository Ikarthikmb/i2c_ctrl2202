#!/bin/env python3
#-------------------------------------------------------------------------
# sky130_gen_sealring.py ---  a seal ring generator for the Google/SkyWater
# sky130 PDK using magic.
#
# Because the seal ring contains many layers that do not appear in standard
# layout editing, they are all specially implemented in the sky130seal_ring.tech
# file in this directory.
#
# An example seal ring was generated by SkyWater and imported using magic's
# gdsquery.sh script.  It was then hand-edited to contain only the bottom
# quarter.  Then it was saved in .mag databases.
#
# The generator script sky130_gen_sealring.py calls magic using the
# sky130seal_ring.tech file, and automatically modifies the geometry to
# stretch to the half width and height of the specified dimensions.  Then
# the lower-left cells are copied and folded over the centerline to make
# the complete seal ring.  The seal ring is then written out in GDS format.
# Then a simplified magic view is generated in the usual user-facing sky130
# technology file, with the GDS_FILE property pointing to the seal ring GDS.
# This layout and GDS can then be imported into a layout.
#
# Note:  All magic files are in base units of centimicrons.  Because the
# manufacturing grid is 5nm, if the half-width of the seal ring is on 5nm,
# the seal ring quadrants will overlap at the center by 5nm, which is not
# an issue.
#
# Usage:
#
#   sky130_gen_sealring.py width height target_dir [-force] [-outer] [-keep]
#
# Where:
#   width = the full-chip layout width
#   height = the full-chip layout height
#   target_dir = location of the full-chip layout
#
#   -force = overwrite any existing files at the target
#   -outer = width and height are the seal ring outer edge, not the chip area
#   -keep = keep local working directory of results
#
# Results:
#   Files advSeal_6um_gen.mag and advSeal_6um_gen.gds are generated and placed in
#   target_dir.  advSeal_6um_gen.mag is an "abstract" view that represents the
#   seal ring in diffusion and the nikon cross in metal1, and references
#   the advSeal_6um_gen.gds file in the same directory as a GDS_FILE property.
#-------------------------------------------------------------------------

import subprocess
import shutil
import sys
import os
import re

def generate_sealring(width, height, target_dir, force, keep):

    starting_dir=os.getcwd()
    
    # Find directory where the script and relevant files exists
    
    abspath = os.path.abspath(__file__)
    script_dir = os.path.dirname(abspath)
    
    # All files of interest are listed below.
    
    script = 'generate_gds.tcl'
    tech = 'sky130seal_ring.tech'
    corner = 'seal_ring_corner.mag'
    abstract = 'seal_ring_corner_abstract.mag'
    slots = 'sealring_slots.mag'
    array = 'seal_ring_slots_array.mag'
    nikon = 'nikon_sealring_shape.mag'
    polygons = ['sr_polygon00007.mag',
	    'sr_polygon00027.mag', 'sr_polygon00011.mag', 'sr_polygon00028.mag',
	    'sr_polygon00001.mag', 'sr_polygon00015.mag', 'sr_polygon00031.mag',
	    'sr_polygon00002.mag', 'sr_polygon00016.mag', 'sr_polygon00032.mag',
	    'sr_polygon00003.mag', 'sr_polygon00019.mag', 'sr_polygon00035.mag',
	    'sr_polygon00004.mag', 'sr_polygon00020.mag', 'sr_polygon00036.mag',
	    'sr_polygon00005.mag', 'sr_polygon00023.mag', 'sr_polygon00039.mag',
	    'sr_polygon00006.mag', 'sr_polygon00024.mag']
        
    # Tries to create 'temp' directory
    
    temp_dir='temp'
    
    if os.path.exists('temp'):
    	print('temp/ directory already exists, trying to create /tmp/sky130_sealring...')
    	temp_dir='/tmp/sky130_sealring'
    else:
    	try:
    	    os.makedirs('temp')
    	except:
    	    print('Couldn\'t create the temp/ directory, trying to create /tmp/sky130_sealring...')
    	    temp_dir='/tmp/sky130_sealring'
    
    # Tries to create /tmp/sky130_sealring if 'temp' is unavailable

    if temp_dir!='temp':
        try:
            if os.path.exists(temp_dir):
                error='Couldn\'t delete files from /tmp/sky130_sealring'
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    os.unlink(file_path)
            else:
                error='Couldn\'t create /tmp/sky130_sealring'
                os.makedirs(temp_dir)
        except:
            print(error)
            sys.exit(1)

    
    os.chdir(temp_dir)
    
    # Copy all .mag files, .magicrc file, and sky130seal_ring.tech file to temp/
    files_to_copy = polygons[:]
    files_to_copy.append(nikon)
    files_to_copy.append(slots)
    files_to_copy.append(array)
    files_to_copy.append(corner)
    files_to_copy.append(abstract)
    files_to_copy.append(tech)
    files_to_copy.append(script)

    for file in files_to_copy:
        shutil.copy(script_dir +"/" + file, '.')

    # Seal ring is placed 6um outside of the chip, so add 12um to width and height
    fwidth = float(width) + 12
    fheight = float(height) + 12

    dbhwidth = round(fwidth * 100)
    dbhheight = round(fheight * 100)

    swidth = str(dbhwidth)
    sheight = str(dbhheight)

    swidthx5 = str(dbhwidth * 5)

    dwidth = str(int(fwidth * 200))
    dheight = str(int(fheight * 200))

    # Modify every polygon to half width and height

    for file in polygons:
        with open(file, 'r') as ifile:
            maglines = ifile.read().splitlines()

        with open(file, 'w') as ofile:
            for line in maglines:
                newline = re.sub('51200', swidth, line)
                newline = re.sub('51210', sheight, newline)
                # NOTE: polygon 39 is at scale 10, not 2, due to
                # corner positions of 45 degree angled geometry.
                newline = re.sub('256000', swidthx5, newline)
                print(newline, file=ofile)

    # Abstract corner view gets the same treatment

    qwidth = str(round(fwidth * 50))
    qheight = str(round(fheight * 50))

    with open(abstract, 'r') as ifile:
        maglines = ifile.read().splitlines()

    with open(abstract, 'w') as ofile:
        for line in maglines:
            newline = re.sub('25600', qwidth, line)
            newline = re.sub('25605', qheight, newline)
            print(newline, file=ofile)

    # Slots arrays are recalculated to span the width and height

    with open(array, 'r') as ifile:
        maglines = ifile.read().splitlines()

    slotsX = False
    with open(array, 'w') as ofile:
        for line in maglines:
            newline = line
            if 'slots_X' in line:
                slotsX = True
            elif 'array 0' in line:
                if slotsX:
                    nslots = int((fwidth - 25.0) / 25.0) - 1
                    newline = 'array 0 ' + str(nslots) + ' 5000 0 0 430'
                else:
                    nslots = int((fheight - 25.0) / 25.0) - 1
                    newline = 'array 0 ' + str(nslots) + ' 5000 0 0 430'

            print(newline, file=ofile)

    # Corner cell changes bounding boxes to half width and height.

    with open(corner, 'r') as ifile:
        maglines = ifile.read().splitlines()

    slotsX = False
    with open(corner, 'w') as ofile:
        for line in maglines:
            newline = re.sub('51200', swidth, line)
            newline = re.sub('51210', sheight, newline)
            print(newline, file=ofile)

    # Create a new top-level layout called 'advSeal_6um_gen.mag'
    # Mirrors uses in X and Y, and adds slots arrays at lower left
    # and upper right

    with open('advSeal_6um_gen.mag', 'w') as ofile:
        print('magic', file=ofile)
        print('tech sky130seal_ring', file=ofile)
        print('magscale 1 2', file=ofile)
        print('timestamp 1584630000', file=ofile)

        # Lower left original
        print('use seal_ring_corner seal_ring_corner_0', file=ofile)
        print('timestamp 1584562315', file=ofile)
        print('transform 1 0 0 0 1 0', file=ofile)
        print('box -30480 -30480 ' + swidth + ' ' + sheight, file=ofile)

        # Mirrored in X
        print('use seal_ring_corner seal_ring_corner_3', file=ofile)
        print('timestamp 1584562315', file=ofile)
        print('transform -1 0 ' + dwidth + ' 0 1 0', file=ofile)
        print('box -30480 -30480 ' + swidth + ' ' + sheight, file=ofile)
	
        # Mirrored in Y
        print('use seal_ring_corner seal_ring_corner_1', file=ofile)
        print('timestamp 1584562315', file=ofile)
        print('transform 1 0 0 0 -1 ' + dheight, file=ofile)
        print('box -30480 -30480 ' + swidth + ' ' + sheight, file=ofile)

        # Mirrored in both X and Y 
        print('use seal_ring_corner seal_ring_corner_2', file=ofile)
        print('timestamp 1584562315', file=ofile)
        print('transform -1 0 ' + dwidth + ' 0 -1 ' + dheight, file=ofile)
        print('box -30480 -30480 ' + swidth + ' ' + sheight, file=ofile)

        # Lower left slot arrays (bottom and left sides slots)
        print('use seal_ring_slots_array seal_ring_slots_array_0', file=ofile)
        print('timestamp 1584629764', file=ofile)
        print('transform 1 0 0 0 1 0', file=ofile)
        print('box 285 285 ' + swidth + ' ' + sheight, file=ofile)

        # Upper right slot arrays (top and right sides slots)
        print('use seal_ring_slots_array seal_ring_slots_array_1', file=ofile)
        print('timestamp 1584629764', file=ofile)
        print('transform -1 0 ' + dwidth + ' 0 -1 ' + dheight, file=ofile)
        print('box 285 285 ' + swidth + ' ' + sheight, file=ofile)

        print('<< end >>', file=ofile)
    
    # Create a new abstract layout TO BE called 'advSeal_6um_gen.mag'
    # This is the view in technology sky130A.  Since there is already
    # a cell with this name that is used to generate GDS, the cell
    # will be called "seal_ring.mag" and copied to "advSeal_6um_gen.mag"
    # in the target directory.

    xwidth = str(dbhwidth)
    xheight = str(dbhheight)

    with open('seal_ring.mag', 'w') as ofile:
        print('magic', file=ofile)
        print('tech sky130A', file=ofile)
        print('timestamp 1584566829', file=ofile)

        # Lower left original
        print('use seal_ring_corner_abstract seal_ring_corner_abstract_0', file=ofile)
        print('timestamp 1584566221', file=ofile)
        print('transform 1 0 0 0 1 0', file=ofile)
        print('box 0 0 ' + qwidth + ' ' + qheight, file=ofile)

        # Mirrored in X
        print('use seal_ring_corner_abstract seal_ring_corner_abstract_3', file=ofile)
        print('timestamp 1584566221', file=ofile)
        print('transform -1 0 ' + xwidth + ' 0 1 0', file=ofile)
        print('box 0 0 ' + qwidth + ' ' + qheight, file=ofile)
	
        # Mirrored in Y
        print('use seal_ring_corner_abstract seal_ring_corner_abstract_1', file=ofile)
        print('timestamp 1584566221', file=ofile)
        print('transform 1 0 0 0 -1 ' + xheight, file=ofile)
        print('box 0 0 ' + qwidth + ' ' + qheight, file=ofile)

        # Mirrored in both X and Y 
        print('use seal_ring_corner_abstract seal_ring_corner_abstract_2', file=ofile)
        print('timestamp 1584566221', file=ofile)
        print('transform -1 0 ' + xwidth + ' 0 -1 ' + xheight, file=ofile)
        print('box 0 0 ' + qwidth + ' ' + qheight, file=ofile)

        print('<< properties >>', file=ofile)
        print('string LEFview no_prefix', file=ofile)
        print('string GDS_FILE advSeal_6um_gen.gds', file=ofile)
        print('string GDS_START 0', file=ofile)
        print('string FIXED_BBOX 0 0 ' + swidth + ' ' + sheight, file=ofile)

        print('<< end >>', file=ofile)

    # Create the GDS of the seal ring

    mproc = subprocess.run(['magic', '-dnull', '-noconsole',
	    'generate_gds.tcl'],
	    stdin = subprocess.DEVNULL, stdout = subprocess.PIPE,
	    stderr = subprocess.PIPE, universal_newlines = True)
    if mproc.stdout:
        for line in mproc.stdout.splitlines():
            print(line)
    if mproc.stderr:
        print('Error message output from magic:')
        for line in mproc.stderr.splitlines():
            print(line)
    if mproc.returncode != 0:
        print('ERROR:  Magic exited with status ' + str(mproc.returncode))

    # Copy the GDS file and the abstract view to the target directory

    os.chdir(starting_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print('Installing files to ' + target_dir)
    if force or not os.path.exists(target_dir + '/advSeal_6um_gen.gds'):
        shutil.copy(temp_dir+'/advSeal_6um_gen.gds', target_dir)
    else:
        print('ERROR: advSeal_6um_gen.gds already exists at target!  Use -force to overwrite.')
    if force or not os.path.exists(target_dir + '/advSeal_6um_gen.mag'):
        shutil.copy(temp_dir+'/seal_ring.mag', target_dir + '/advSeal_6um_gen.mag')
    else:
        print('ERROR: advSeal_6um_gen.mag already exists at target!  Use -force to overwrite.')
    if force or not os.path.exists(target_dir + '/seal_ring_corner_abstract.mag'):
        shutil.copy(temp_dir+'/seal_ring_corner_abstract.mag', target_dir)
    else:
        print('ERROR: seal_ring_corner_abstract.mag already exists at target!  Use -force to overwrite.')
    
    # Remove the temporary directory and its contents
    
    if not keep:
        shutil.rmtree(temp_dir)
    else:
        print('Retaining generated files in '+temp_dir+'/ directory')

    # Done!
    print('Done generating files advSeal_6um_gen.gds and advSeal_6um_gen.mag in ' + target_dir)
    print('Place the seal ring cell in the final layout at (0um, 0um) before generating GDS.')
    print('The top level layout minus seal ring must have a lower left corner of (6um, 6um)')

# If called as main, run generate_sealring()

if __name__ == '__main__':

    # Divide up command line into options and arguments
    options = []
    arguments = []
    for item in sys.argv[1:]:
        if item.find('-', 0) == 0:
            options.append(item)
        else:
            arguments.append(item)

    force = True if '-force' in options else False
    keep = True if '-keep' in options else False
    outer = True if '-outer' in options else False

    # Need one argument:  path to verilog netlist
    # If two arguments, then 2nd argument is the output file.

    if len(arguments) == 3:
        width = arguments[0]
        height = arguments[1]
        target_dir = arguments[2]

        # Seal ring is 12um thick, so if "outer" option is used, subtract 12um
        # from both width and height.
        if outer:
            width = str(float(width) - 12.0)
            height = str(float(height) - 12.0)

        generate_sealring(width, height, target_dir, force, keep)
    else:
        print("Usage:  sky130_gen_sealring.py <width> <height> <target_dir> [options]")
        print("Options:")
        print("   -outer : Width and height are seal ring outer edge, not chip area")
        print("   -force : Overwrite any existing files at <target_dir>")
        print("   -keep :  Keep generated files in temp/ directory")
    

