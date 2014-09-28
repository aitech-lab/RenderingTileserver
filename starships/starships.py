
import sys, os, bpy, bmesh
from random import random,randint
sys.path.append(os.path.dirname(bpy.data.filepath))

from bottle import route, run, template, static_file
from shutil import rmtree
from time import sleep

def get_random_material():
    index = randint(0, len(bpy.data.materials)-1)
    return bpy.data.materials[index]
    
def generate_starship():

    bpy.ops.object.mode_set(mode = 'OBJECT')
    # clean old cube
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_pattern(pattern="Cube*")
    bpy.ops.object.delete()

    bpy.ops.mesh.primitive_cube_add(
        radius=0.25, location=(0,0,0)
    )

    # bpy.ops.object.editmode_toggle()
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True) # force edges
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.subdivide(number_cuts=3)
    for i in range(5): 
        bpy.context.object.data.materials.append(get_random_material())

    bpy.ops.mesh.select_all(action="DESELECT")

    bpy.context.object.update_from_editmode()
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)

    bpy.context.tool_settings.mesh_select_mode = (True, False, False) # force edges

    for v in bm.verts:
        if v.co.x<0: 
            v.select = True 
    bpy.ops.mesh.delete(type='VERT')
      
    bpy.context.tool_settings.mesh_select_mode = (False, False, True) # force edges

    # #bmesh.update_edit_mesh(me, True)
    # #bpy.ops.mesh.select_all(action="DESELECT")
    # #bpy.ops.mesh.select_random(action='DESELECT', percent=75)

    for i in range(0, 5):
        bpy.ops.object.mode_set(mode = 'EDIT')    # Return to object mode</pre>
        
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.mesh.select_random(action='SELECT', percent=5)
        bpy.ops.mesh.subdivide(number_cuts=1)
        bpy.ops.mesh.extrude_region_shrink_fatten(
            TRANSFORM_OT_shrink_fatten={
                "value":-(0.2+random()),
                "proportional":'ENABLED'
            })
    
        bpy.ops.object.mode_set(mode = 'OBJECT')    # Return to object mode</pre>
            
        for p in bpy.context.object.data.polygons:
            if p.select: p.material_index = randint(0,4)

    bpy.ops.object.modifier_add(type='MIRROR') 
    bpy.ops.object.modifier_add(type='LAPLACIANSMOOTH')
    bpy.context.object.modifiers["Laplacian Smooth"].lambda_factor = 5.0


    #bpy.ops.object.editmode_toggle()

# -63.434948822922010648427806279547
# 0 0.5 1.5 3.5
# 0 1   2   3
@route('/tile/<z>/<x>/<y>')
def index(z=0,x=0,y=0):

    path = os.path.join(os.path.dirname(bpy.data.filepath), "tiles", z, x)
    name = '%s.png' % y
    image = os.path.join(path, name)
    
    if not os.path.exists(image):

        size = 2**int(z)
        
        x = int(x) % size
        y = int(y) % size
        z = int(z) % 20
        
        name = '%d-%d-%d' % (z,x,y)

        generate_starship()

        cam = bpy.data.objects['Camera']

        # cam.location.x = x*10
        # cam.location.y = (size-y-1)*20

        #bpy.data.cameras['Camera'].ortho_scale = 128 / size
        
        if not os.path.exists(path): 
            os.makedirs(path)
        
        cam.name = name
        bpy.data.scenes["Scene"].render.filepath = image
        bpy.context.scene.render.resolution_x = 256 #perhaps set resolution in code
        bpy.context.scene.render.resolution_y = 256
        bpy.ops.render.render(write_still=True)
        cam.name = "Camera"
        print('send %s' % name)
        print(os.path.exists(image))   

    return static_file(image, root=path, mimetype='image/jpeg')

tiles = os.path.join(os.path.dirname(bpy.data.filepath), "tiles")
if os.path.exists(tiles): rmtree(tiles)

run(host='localhost', port=9090)
