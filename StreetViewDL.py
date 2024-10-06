import re, os, sys, urllib.request, urllib.error, argparse
from sys import platform

args = None
map_id = None
x_values_max = 0
y_values_max = 0
zoom_val = 5
base_url = 'https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid='

class MyParser(argparse.ArgumentParser):
	def error(self, message):
		sys.stderr.write('error: %s\n' % message)
		self.print_help()
		sys.exit(2)

def setupArguments():
	parser = MyParser()
	parser.add_argument('url',type=str)
	parser.add_argument('--prefix',type=str,default='', help='e.g.: 2018-05')
	parser.add_argument('--filename',type=str,default='', help='optional. if omitted pano_id.png is the filename.')

	global args
	args = parser.parse_args()

def create_folder():
	os.makedirs(map_id,exist_ok=True)
	os.makedirs(map_id+'/tiles',exist_ok=True)
	os.chdir(map_id+'/tiles')

def extract_panoid():
	print("extract_panoid")
	match = re.search(r"panoid%3D(.*?)%", args.url)
	if match:
		return match.group(1)
	else:
		print("Error: Couldn't extract panoid")
		sys.exit(2)

def test_image_url(url):
	# print('test_image_url: ',url)
	try:
		conn = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		# Return code error (e.g. 404, 501, ...)
		# ...
		# print('HTTPError: {}'.format(e.code))
		return False
	except urllib.error.URLError as e:
		# Not an HTTP-specific error (e.g. connection refused)
		# ...
		# print('URLError: {}'.format(e.reason))
		return False
	else:
		# 200
		# ...
		# print('good')
		return True

def generate_download_url(x,y):
	return base_url+map_id+'&x='+str(x)+'&y='+str(y)+'&zoom='+str(zoom_val)+'&nbt=1&fover=2'

def download_tile(x,y):
	print('dl tile: ',x,y)
	img_data = urllib.request.urlopen(generate_download_url(x,y)).read()
	with open(str(y).zfill(2)+'_'+str(x).zfill(2)+'.png', 'wb') as handler:
		handler.write(img_data)

def determine_x_range():
	print('determine_x_range')
	global x_values_max
	for x_val in range(0,999):
		image_url = generate_download_url(x_val,0)
		if test_image_url(image_url) == True:
			if x_val>y_values_max:
				x_values_max = x_val
			download_tile(x_val,0)
		else:
			# url doesn't exist
			break

def determine_y_range():
	print('determine_y_range')
	global x_values_max, y_values_max
	for y_val in range(1,999):
		image_url = generate_download_url(0,y_val)
		if test_image_url(image_url) == True:
			if y_val>y_values_max:
				y_values_max = y_val
			download_tile(0,y_val)
		else:
			# url doesn't exist
			break

def download_remaining_tiles():
	print('download_remaining_tiles')
	global x_values_max, y_values_max
	for x_val in range(1,x_values_max+1):
		for y_val in range(1,y_values_max+1):
			image_url = generate_download_url(x_val,y_val)
			if test_image_url(image_url) == True:
				if y_val>y_values_max:
						y_values_max = y_val
				download_tile(x_val,y_val)
			else:
				# url doesn't exist
				break

def get_output_filename():
	if len(args.filename) > 0:
		return args.filename
	elif len(args.prefix) > 0:
		return args.prefix+'_'+map_id+'.png'
	else:
		return map_id+'.png'

def run_montage():
	print('run_montage')
	monatage_files = ''
	for y in range(0,y_values_max+1):
		for x in range(0,x_values_max+1):
			monatage_files = monatage_files + str(y).zfill(2)+'_'+str(x).zfill(2)+'.png '
	if 'linux' not in platform:
		montage_call = 'magick montage '+monatage_files+' -tile '+str(x_values_max+1)+'x'+str(y_values_max+1)+' -geometry 512x512+0+0 png24:../'+get_output_filename()
	else:
		montage_call = 'montage '+monatage_files+' -tile '+str(x_values_max+1)+'x'+str(y_values_max+1)+' -geometry 512x512+0+0 png24:../'+get_output_filename()
	print(montage_call)
	os.system(montage_call)

if __name__ == '__main__':
	setupArguments()
	map_id = extract_panoid()
	create_folder()
	determine_x_range()
	determine_y_range()
	print(x_values_max,y_values_max)
	download_remaining_tiles()
	run_montage()