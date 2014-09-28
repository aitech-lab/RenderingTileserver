
import sys, os, bpy
sys.path.append(os.path.dirname(bpy.data.filepath))

from bottle import route, run, template, static_file
from shutil import rmtree
from time import sleep

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
		
		name = '%d/%d/%d' % (z,x,y)

		cam = bpy.data.objects['Camera']

		cam.location.x = x*2
		cam.location.y = (size-y-1)*4

		#bpy.data.cameras['Camera'].ortho_scale = 128 / size
		
		if not os.path.exists(path): 
			os.makedirs(path)
		cam.name = name
		bpy.data.scenes["Scene"].render.filepath = image
		bpy.ops.render.render(write_still=True)
		cam.name = "Camera"
		print('send %s' % name)
		print(os.path.exists(image))		
	return static_file(image, root=path, mimetype='image/jpeg')

tiles = os.path.join(os.path.dirname(bpy.data.filepath), "tiles")
if os.path.exists(tiles): rmtree(tiles)

run(host='localhost', port=9090)
