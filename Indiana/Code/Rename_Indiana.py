import os, shutil, datetime, csv
import xlrd
import ghostscript
from wand.image import Image
#from PIL import Image

one_slice = .4
two_slice = .6
threshold = .08

input_path = "D:\\Dropbox (UChicago)\\MFG Project\\raw_data_copies\\Indiana_scans"
output_path = "D:\\Dropbox (UChicago)\\MFG Project\\manuscript_database\\IN\\Output_final"

remove = ['.dropbox']
no_excel = ['.xls', '.xlsx']
not_for_dir = ['?']

#a recursive stratregy is best
def collect(input_path):

	#base case
	if os.path.isdir(input_path) == False:
		#return {'root' : input_path}
		x = 'root'
		return x
	#recursive case
	else:
		folder_contents = os.listdir(input_path)
	
		if remove[-1] in folder_contents:
			for x in remove:
				if x in folder_contents:
					folder_contents.remove(x)
		current_dictionary = {}
		for element in folder_contents:
			current_path = input_path + "\\" + element
			lower_dictionary = collect(current_path)
			current_dictionary[element] = lower_dictionary
		return current_dictionary


def populate(dictionary, current_path):
	keys = list(dictionary.keys())

	if 'root' in list(dictionary.values()):
		for key in keys:
			#rel_path = os.path.relpath(current_path + key, input_path)
			#print('current', current_path)
			old_path = current_path + "\\" + key
			#print('rel', rel_path)
			if os.path.isdir(old_path):
				
				next_path = old_path
				populate(dictionary[key], next_path)
				continue
			file_raw = old_path.rsplit("\\", 1)
			#print(file)
			

			meta = file_raw[-1].split("gray")
			file_num = meta[1]
			state = "IN"
			county = ""
			year = '1880'		
			

			new_dir = output_path 
			for i in [year]:
				new_dir = new_dir + "\\" + i
				if os.path.isdir(new_dir) == False:
					os.makedirs(new_dir)
			
			file = "_".join([state, year, county, file_num])
			new_path = new_dir + "\\" + file
			
			#print(old_path, new_path)
			format_img(old_path, new_path)
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			rel_path = os.path.relpath(next_path, input_path)
			new_dir = output_path + "\\" + rel_path
		
			if os.path.isdir(next_path):
				populate(dictionary[key], next_path)



#only used for PDF conversions

def format_img(old_path, new_path):
	with Image(filename = old_path) as img:
		width = img.width
		height = img.height
		#if width > height: #this is just a baseline criteria for determining if doc has two pages
		if width > height and float(width - height)/float(height) > threshold:
			img.format = 'jpeg'
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
			img.format = 'jpeg'
			file_path, filetype = os.path.splitext(new_path)
			if os.path.isfile(file_path + "_S" +'.jpg') == False:
				img.save(filename = file_path + "_S" +'.jpg')
			#shutil.copy(old_path, new_path)


######################################################################
if __name__ == '__main__':
	dictionary = collect(input_path)
	#print(dictionary)
	populate(dictionary, input_path)