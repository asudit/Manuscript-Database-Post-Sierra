# exec(open("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Code\\MO_Rename.py").read()) 

import os, shutil, datetime, sys
import csv, wand, xlrd
#sys.path.insert(0, "C:\\Program Files\\ImageMagick-7.0.3-Q16")
from PIL import Image


one_slice = .4
two_slice = .6
threshold = .08

input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Input\\Missouri_copy"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Output_final"
csv_name_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Renaming_metadata"

#metadata_xlsx = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Renaming_metadata\\MO_7_S1_metadata_edited.xlsx"
metadata_xlsx =  "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Renaming_metadata\\MO_8_S1_metadata.xlsx"
#metadata_xlsx = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Renaming_metadata\\MO_5_S1_metadata.xlsx"
#metadata_xlsx = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Renaming_metadata\\MO_6_S1_metadata.csv"

temp_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Temp"
test_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Input\\Missouri_copy\\1860 Social Statistics Schedule"
package_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Packages"

remove = ['1860 Social Statistics Schedule', 'Title Targets', 'Thumbs.db']


def collect(input_path):
	#base case
	if os.path.isdir(input_path) == False:
		x = 'root'
		return x
	#recursive case
	else:
		folder_contents = os.listdir(input_path)
		#print(folder_contents)
		for x in remove:
			if x in folder_contents:
				folder_contents.remove(x)
		current_dictionary = {}
		for element in folder_contents:
			#print(element)
			current_path = input_path + "\\" + element
			lower_dictionary = collect(current_path)
			current_dictionary[element] = lower_dictionary
		return current_dictionary


def populate(old_dictionary, current_path, output_path, regenerate, bad_cut_list, empty_list):
	#print(current_path)
	keys = list(old_dictionary.keys())
	#print(keys)
	if old_dictionary[keys[0]] == 'root':
		for key in keys:
			old_path = current_path + "\\" + key
			meta = key.split("_")
			#a strange exception when meta = ['0000000.tif']
			if len(meta) == 1:
				continue
			state = "MO"
			#print(meta)
			year = meta[2]
			county = meta[-2]
			file_num_and_type = meta[-1].split(".")
			
			#these counties are named incorrectly in the raw files
			if county == '0Ray':
				county = 'Ray'
			if county == '1870' and 'Ripley' in old_path:
				county = 'Ripley'
			if county == '1860' and 'StLouis' in old_path:
				county = 'StLouis'
			if county == '1860' and 'Callaway' in old_path:
				county == 'Callaway'
			if county == 'VOL1':
				continue
			
			#print(meta)

			file_num = file_num_and_type[0]
			file_type = file_num_and_type[1]
			file_num_length = len(file_num)
			file_num_4 = '0' * (5 - file_num_length) + file_num
			filename = "_".join([state, year[2], county, file_num_4])

			new_path = output_path
			for x in [state, year, county]:
				new_path = new_path + "\\" + x
				if os.path.isdir(new_path) == False:
					os.makedirs(new_path)
			new_path = new_path + "\\"+ filename + "." + file_type
			#shutil.copy(old_path, new_path + "\\"+ filename + "." + file_type)
			if regenerate:
				#print('regenerating')
				bad_cut(old_path, new_path, filename, state, year, bad_cut_list, empty_list, "_S")
				continue

			format_img(old_path, new_path)
  
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			populate(old_dictionary[key], next_path, output_path)
		#return new_dictionary



def read_metadata(metadata_csv):
	bad_cut_list = []
	empty_list = []
	bad_cut = 5
	empty = 6
	file = 2
	with open(metadata_csv, 'rt') as f:
		rows = csv.reader(f)
		rows.next()
		for row in rows:
			if row[bad_cut] == '1':
				bad_cut_list.append(row[file])
			if row[empty] != "":
				empty_list.append(row[file])
	return bad_cut_list, empty_list

def csv_metadata(metadata_xlsx, csv_name_output, dictionary, state, year):
	'''
	This function will take the metadata csv the undergrads made, and use it to make a master renaming csv.
	This new csv will include a new name for each file. I guess dictionary will only be needed when we actually rename the file
	'''
	new_csv_list = []
	if 'xlsx' in metadata_xlsx:
		workbook = xlrd.open_workbook(metadata_xlsx)
		sheet = workbook.sheet_by_name('Sheet1')
		metadata_csv = open(csv_name_output + "\\" + state + "_" + year + '.csv', "wb")
		writer = csv.writer(metadata_csv)
		for row in list(range(sheet.nrows)):
			#print(sheet.row_values(row))
			writer.writerow(sheet.row_values(row))
		metadata_csv.close()
	else:
		shutil.copy(metadata_xlsx, csv_name_output + "\\" + state + "_" + year + '.csv')
	#print(metadata_csv)
	with open(csv_name_output + "\\" + state + "_" + year + '.csv', 'rt') as f:
		file = csv.reader(f)
		file.next()
		for row in file:
			new_year, old_file, new_county, bad_cut_indicator, empty_indicator = row[1], row[2], row[3], row[5], row[6]
			schedule, page_no , establishment_count, legibility = row[7], row[8] ,row[9], row[11]
			#MO 1850, collector notes some unusual stuff in these columns, when not marked as "1"
			notes = row[13]
			if len(row) == 15:
				notes_additonal = row[14]
			old_name, old_type = os.path.splitext(old_file)
			#the old filenames have to match the ones in the actual directory -- the ones in the directory have labels, those in the csv do not
			old_file = old_name + "_S" + old_type
			worse_version = ""
			duplicate = ""
			crossed_out = ""
			unusual_file = ""
			#since there is no whitespace for MO, I will treat every file with a not blank "empty" column the same
			no_data_file = ""
			if empty_indicator != "":
				no_data_file = '1'
			whitespace_file = ""
			information_not_attainable = ""
			#for other files, a whitespace indicator variable will be needed; here none of the files were cut so not needed
			#corrupted file is for files that are actually corrupted/ difficult to collect data on (maybe we can set a threshold on legibility for corruption)
			filename, filetype = os.path.splitext(old_file)
			meta = filename.split("_")
			
			if len(meta) < 4:
				print(meta)
				continue
			filenum =  meta[3]
			#we only want the file to be 6 characters long, to be safe
			if len(filenum) >6:
				filenum = filenum[:6]
			#if the old file is not labelled with source, we need to add it to match later with actual files
			if len(meta) == 4:
				meta.append("S")
				filename = "_".join(meta)
			
			if year == '1850':
				for i in [notes, notes_additonal]:
					#print(i)
					#number is a float, not int for some reason
					if i != "1.0" and i != "":
						unusual_file = '1'
						break
			#MO 1870 has a lot of weird stuff. See documentation
			if year == "1870":
				#case 1: worse duplicate/version
				
				if bad_cut_indicator != "":
					if filenum.endswith("a") or filenum.endswith("b"):
						worse_version = "1"
					else:
						unusual_file = "1"
			
			if year == "1880":
				if bad_cut_indicator != "":
					unusual_file = "1"
			#No splitting, so 1half or whatever not needed
			new_file = "_".join([state, new_year[2], new_county.lower(), filenum, 'S.jpg'])
			new_csv_list.append([old_file, new_file, no_data_file, whitespace_file ,unusual_file, worse_version, duplicate, crossed_out, schedule, page_no, establishment_count, legibility, information_not_attainable])
	if os.path.isdir(csv_name_output + "\\" + state) == False:
		os.makedirs(csv_name_output + "\\" + state)
	with open(csv_name_output + "\\" + state + "\\" + year + '.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['old_file','new_file', 'no_data', 'whitespace' ,'unusual_file', 'worse_version', 'duplicate', 'Nullified/Crossed_Out', 'schedule','page_no' ,'establishment_count', 'legibility','info_not_attainable'])
		for row in new_csv_list:
			writer.writerow(row)






				



	


#############No recutting needed for MO (see documentation). Marking/generating CSV's will be done in another function
'''
def bad_cut(old_path, new_path, filename, state, year, bad_cut_list, empty_list, underscore_stamp):
	transfer_path = new_path.rsplit("\\", 1)
	#for two halfs, in case of splitting 
	filename, filetype = os.path.splitext(transfer_path[1])
	regenerate_path = regenerate_output_path + "\\" + state + "\\" + year + "\\" + transfer_path[1]
	if os.path.isdir(regenerate_output_path + "\\" + state + "\\" + year) == False:
		os.makedirs(regenerate_output_path + "\\" + state + "\\" + year)
	
	#why two of everything? because the files in the csv have no stamp, but the actuall file
	#in the output folder does
	new_file0_stamped = filename + underscore_stamp + '.jpg'
	new_file0 = filename + '.jpg'
	new_file1_stamped = filename + "_" + '1half' + underscore_stamp + '.jpg'
	new_file1 = filename + "_" + '1half' + '.jpg'
	new_file2_stamped = filename + "_" + '2half' + underscore_stamp + '.jpg'
	new_file2 = filename + "_" + '2half' + '.jpg'
	#if 'IA' in filename and '8' in filename:
	#print(new_file1)

	#if both files are marked as bad cut I assume I need to regenerate them completely
	if new_file1 in bad_cut_list and new_file2 in bad_cut_list:
		print(new_file1)
		for i in [(new_file1, new_file1_stamped), (new_file2, new_file2_stamped)]:
			#make list of bad files shorter once processes
			#print(i[0])
			#bad_cut_list.remove(i[0])
			#delete file from output folder
			if os.path.isfile(transfer_path[0] + "\\" + i[1]):
				os.remove(transfer_path[0] + "\\" + i[1])
			#print('Delete bad cuts file:\n\n',transfer_path[0] + "\\" + i[1])
		#regenerate in main output folder
		
		format_img(old_path, new_path)
		
		#regenerate in regenerate output folder to make packaging easier
		
		format_img(old_path, regenerate_path)
		#print('New output folder too:\n\n', regenerate_path)
	
	#here I assume this means that the first or second half is white space, and thus no splitting is needed. 
	# elif makes sure that both cannot be white space
	elif new_file1 in bad_cut_list or new_file2 in bad_cut_list:
		for i in [(new_file1, new_file1_stamped), (new_file2, new_file2_stamped)]:
			#bad_cut_list.remove(i[0])
			#delete file from output folder
			if os.path.isfile(transfer_path[0] + "\\" + i[1]):
				os.remove(transfer_path[0] + "\\" + i[1])
		#we take the old file, and now we want to convert it to jpeg, output it to both the output folder and the regenerate folder,
		# all without splitting it
		for output_folder in [new_path, regenerate_path]:
			img = Image.open(old_path)
			filename, filetype = os.path.splitext(output_folder)
			if os.path.isfile(filename + underscore_stamp + '.jpg') == False:
				img.save(filename + underscore_stamp + '.jpg')


	# it is possible that either or both of the split files have no metadata
	for i in [(new_file1 ,new_file1_stamped), (new_file2 ,new_file2_stamped)]:
		if i[0] in empty_list:
			file, filetype = os.path.splitext(i[1])
			if os.path.isfile(transfer_path[0] + "\\" + i[1]):
				os.rename(transfer_path[0] + "\\" + i[1], transfer_path[0] + "\\" + file + "_" + 'W' + filetype)
				#os.rename(transfer_path[0] + "\\" + file + "_" + 'W' + filetype, transfer_path[0] + "\\" + i)
			#print('Chnaging empty half from:\n', transfer_path[0] + "\\" + i, 'to:\n', transfer_path[0] + "\\" + file + "_" + 'W' + filetype)

	if new_file0 in empty_list:
		file, filetype = os.path.splitext(new_file0_stamped)
		print(transfer_path[0] + "\\" + new_file0_stamped)
		if os.path.isfile(transfer_path[0] + "\\" + new_file0_stamped):
			os.rename(transfer_path[0] + "\\" + new_file0_stamped, transfer_path[0] + "\\" + file + "_" + 'W' + filetype)
		#print('Changing empty sheet name from :\n\n', transfer_path[0] + "\\" + new_file0_stamped, 'to blank label:', transfer_path[0] + "\\" + file + "_" + 'W' + filetype)
		#complex because could be all three empty

		#note --  you also want to regenerate a copy into a separate folder so that they can easily go through it e.g. regenerate one
		#for output final or whatever and one for a folder next to it called regenerate or whatever
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
		if os.path.isfile(transfer_path[0] + "\\" + filename + '_' + '2half' + "_S" + '.jpg') == False:
			image_one.crop((int(width_one), 0, width, height)).save(transfer_path[0] + "\\" + filename + '_' + '2half' + "_S" + '.jpg')
			image_two.crop((0, 0, int(width_two), height)).save(transfer_path[0] + "\\" + filename + '_' + '1half' + "_S" + '.jpg')
	else: 
		file_path, filetype = os.path.splitext(new_path)
		if os.path.isfile(file_path + "_S" + '.jpg') == False:
			img.save(file_path + "_S" + '.jpg')




######################################################################
if __name__ == '__main__':
	#dictionary = collect(input_path)
	#bad_cut_list, empty_list = read_metadata(metadata_csv)
	#populate(dictionary, input_path, output_path, True, bad_cut_list, empty_list)
	csv_metadata(metadata_xlsx, csv_name_output, {}, 'MO', '1880')


	#dictionario = csv_dict(output_path, package_path, {})
	#csv_write(dictionario, package_path)
	