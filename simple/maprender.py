# import http.server
# import socketserver

# PORT = 8000

# Handler = http.server.SimpleHTTPRequestHandler

# httpd = socketserver.TCPServer(("", PORT), Handler)

# print("serving at port", PORT)
# httpd.serve_forever()



# cam = bpy.data.objects['Camera']
# origin = bpy.data.objects['Empty']

# # origin.rotation_euler[2] = radians(step * (360.0 / step_count))

# bpy.data.scenes["Scene"].render.filepath = '/home/user/VR/vr_shot_%d.jpg' % step
# bpy.ops.render.render( write_still=True )

#import bpy
#import os
#print("MAPRENDER")
#cam = bpy.data.objects['Camera']
#bpy.data.scenes["Scene"].render.filepath = os.path.join(os.path.dirname(bpy.data.filepath), "render.jpg")
#bpy.ops.render.render( write_still=True )
#
import sys, os, bpy
sys.path.append(os.path.dirname(bpy.data.filepath))

from bottle import route, run, template, static_file
from shutil import rmtree

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

		offset = (size-1) / size * 64
		cam.location.x =         x  * 128 / size   - offset 
		cam.location.y = (size-1-y) * 128 / size*2 - offset*2 - 173.2

		bpy.data.cameras['Camera'].ortho_scale = 128 / size
		
		if not os.path.exists(path): 
			os.makedirs(path)
		cam.name = name
		bpy.data.scenes["Scene"].render.filepath = image
		bpy.ops.render.render(write_still=True)
		cam.name = "Camera"
	return static_file(name, root=path, mimetype='image/jpeg')

tiles = os.path.join(os.path.dirname(bpy.data.filepath), "tiles")
if os.path.exists(tiles): rmtree(tiles)

run(host='localhost', port=9090)
