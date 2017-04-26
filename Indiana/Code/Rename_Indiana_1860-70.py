# This python file will take Indiana 1860-1870 files and incorporate their meta-data into their file names. 
# The new files are outputed to the "out" folder in IN

# exec(open("D:\\Dropbox (UChicago)\\MFG Project\\manuscript_database\\IN\\Code\\Rename_File_Prelim_IN6070.py").read())
# my execute: exec(open("./filename").read())

#Run time: < 1 s



import os, shutil, datetime, sys
import csv, wand, xlrd
#sys.path.insert(0, "C:\\Program Files\\ImageMagick-7.0.3-Q16")
#from PIL import Image
import ghostscript
from wand.image import Image

one_slice = .4
two_slice = .6
threshold = .08

input_path = "D:\\Dropbox (UChicago)\\MFG Project\\manuscript_database\\IN\\Input\\U.S. Ninth Census of Manufacturers"
output_path = "D:\\Dropbox (UChicago)\\MFG Project\\manuscript_database\\IN\\Output_final"
#regenerate_output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Regenerate_output"
#csv_name_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Renaming metadata"


#metadata_csv_output = "D:\\Dropbox (UChicago)\\MFG Project\\manuscript_database\\IN\\Output_final"

#"D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Temp\\IA_8_A_metadata.csv"

#Csv_crosswalk_folder = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\File Naming Files"

package_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Packages"
#my_path = "\\Users\\Adam\\Pictures\\rho_0.9.png"
#states = {'california': 'CA', 'iowa': 'IA', 'maine':  'ME', 'massachusetts': 'MA', 'nebraska': 'NE', 'new york': 'NY', 'south carolina': 'SC', 'virginia': 'VA'}
#remove = ['coding_example', 'renamed_copies', 'rename_CA - (not working copy)', 'rename_CA', 'rename_IA', 'rename_template', 'readme.rtf', '_checks']

#remove = []

#a recursive stratregy is best
def collect(input_path):
	#print("Current path is:", input_path)

	#base case
	if os.path.isdir(input_path) == False:
		#return {'root' : input_path}
		x = 'root'
		return x
	#recursive case
	else:
		folder_contents = os.listdir(input_path)
		#print(folder_contents)
		#return
		#if remove[-1] in folder_contents:
			#print(folder_contents)
			#for x in remove:
				#if x in folder_contents:
					#folder_contents.remove(x)
		current_dictionary = {}
		for element in folder_contents:
			current_path = input_path + "\\" + element
			lower_dictionary = collect(current_path)
			current_dictionary[element] = lower_dictionary
		return current_dictionary
			

def populate(dictionary, current_path, regenerate, bad_cut_list, empty_list):
	keys = list(dictionary.keys())

	if 'root' in list(dictionary.values()):
		for key in keys:
			rel_path = os.path.relpath(current_path, input_path)
			old_path = current_path + "\\" + key
			if os.path.isdir(old_path):
				#print(old_path)
				next_path = old_path
				populate(dictionary[key], next_path, regenerate, bad_cut_list, empty_list)
				continue
			file_list = rel_path.split("\\")
			file_list.append(key)
			#print(file_list)
			
			#print(file_list)
			#California exception - eliminate township and Industry folder for consistency
			state = 'IN'
			
			county = file_list[1]
			year = file_list[0][2]		
			file_num = file_list[2][4:]

			new_dir = output_path 
			for i in [file_list[0]]:
				new_dir = new_dir + "\\" + i
				if os.path.isdir(new_dir) == False:
					os.makedirs(new_dir)

			
			file = "_".join([state, year, county, file_num])
			new_path = new_dir + "\\" + file

			#this is to do regeneration as needed
			if regenerate:
				#print('regenerating')
				bad_cut(old_path, new_path, file, state, file_list[1], bad_cut_list, empty_list, "_A")
				continue

			#print(file)
		
			format_img(old_path, new_path)
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			rel_path = os.path.relpath(next_path, input_path)
			new_dir = output_path + "\\" + rel_path
			#if os.path.isdir(next_path) and os.path.isdir(new_dir) == False:
			#	os.makedirs(new_dir)
			if os.path.isdir(next_path):
				populate(dictionary[key], next_path, regenerate, bad_cut_list, empty_list)



def format_img(old_path, new_path):
	#with Image(filename = old_path) as img:
	with Image(filename = old_path, resolution=200) as img:
		width = img.width
		height = img.height
		#if width > height: #this is just a baseline criteria for determining if doc has two pages
		if width > height and float(width - height)/float(height) > threshold:
			#img.format = 'jpeg'
			img.compression_quality = 99
			width_one = one_slice * width
			width_two = two_slice * width
			image_one = img[int(width_one):width, 0:height]
			image_two = img[0:int(width_two), 0:height]
			transfer_path = new_path.rsplit("\\", 1)
			#extract file extension
			filename, filetype = os.path.splitext(transfer_path[1])
			if os.path.isfile(transfer_path[0] + "\\" + filename + '_' + '2half' +  "_S" + '.jpg') == False:
				image_one.save(filename = transfer_path[0] + "\\" + filename + '_' + '2half' + "_S" +'.jpg') #we need to check save also take path, not just filename
				image_two.save(filename = transfer_path[0] + "\\" + filename + '_' + '1half' + "_S" + '.jpg')
		else:
			#img.format = 'jpeg'
			img.compression_quality = 99
			file_path, filetype = os.path.splitext(new_path)
			if os.path.isfile(file_path + "_S" +'.jpg') == False:
				img.save(filename = file_path + "_S" +'.jpg')
			#shutil.copy(old_path, new_path)

'''
def format_img(old_path, new_path):
	img = Image.open(old_path)
	width, height  = img.size
	if width > height and abs(float(width - height))/float(height) > threshold:
		transfer_path = new_path.rsplit("\\", 1)
		filename, filetype = os.path.splitext(transfer_path[1])

		width_one = one_slice * width
		width_two = two_slice * width
		image_one, image_two = img, img
		if os.path.isfile(transfer_path[0] + "\\" + filename + '_' + '2half' + "_A" +  '.jpg') == False:
			image_one.crop((int(width_one), 0, width, height)).save(transfer_path[0] + "\\" + filename + '_' + '2half' + "_A" + '.jpg')
			image_two.crop((0, 0, int(width_two), height)).save(transfer_path[0] + "\\" + filename + '_' + '1half' + "_A" + '.jpg')
	else: 
		file_path, filetype = os.path.splitext(new_path)
		if os.path.isfile(file_path + "_A" + '.jpg') == False:
			img.save(file_path + "_A" + '.jpg')
'''
####################################################csv_write and csv_dict have been moved to general code###################################################################


######################################################################

if __name__ == '__main__':
	'''
	folder_contents = os.listdir(csv_name_output)
	for i in range(len(folder_contents)):
		if os.path.isfile(csv_name_output + "\\" +folder_contents[i]):
			name = folder_contents[i].split("_")
			state_abbrev = name[0]
			year = '18' + name[1] + '0'
			csv_metadata(csv_name_output + "\\" +folder_contents[i], csv_name_output, {}, state_abbrev, year)
	'''
	dictionary = collect(input_path)
	#print(dictionary)
	#print(list(dictionary.keys()))
	#bad_cut_list, empty_list = read_metadata([])
	#print(bad_cut_list)
	#print(empty_list)
	populate(dictionary, input_path, False, [], [])
	






