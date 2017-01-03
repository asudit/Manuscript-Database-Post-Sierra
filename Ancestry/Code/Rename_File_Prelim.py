# This python file will take ancestry files and incorporate their meta-data into their file names. 
# The new files are outputed to the "out" folder in ancestry

# exec(open("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Code\\Rename_File_Prelim.py").read())
# my execute: exec(open("./filename").read())
#One issue in the ancestry data is California - it is iiregular in its org - it has an industry foler, and a not stated folder for some counties (Los Angeles). 
#it might be easier to fix this manually

#Run time: < 1 s



import os, shutil, datetime, sys
import csv, wand, xlrd
#sys.path.insert(0, "C:\\Program Files\\ImageMagick-7.0.3-Q16")
from PIL import Image

one_slice = .4
two_slice = .6
threshold = .08

input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\Input\\ancestry_downloads_copy"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output_final"
regenerate_output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Regenerate_output"
csv_name_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Renaming metadata"


#metadata_csv_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Naming Files"

#"D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Temp\\IA_8_A_metadata.csv"

Csv_crosswalk_folder = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\File Naming Files"

package_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Packages"
#my_path = "\\Users\\Adam\\Pictures\\rho_0.9.png"
states = {'california': 'CA', 'iowa': 'IA', 'maine':  'ME', 'massachusetts': 'MA', 'nebraska': 'NE', 'new york': 'NY', 'south carolina': 'SC', 'virginia': 'VA'}
remove = ['coding_example', 'renamed_copies', 'rename_CA - (not working copy)', 'rename_CA', 'rename_IA', 'rename_template', 'readme.rtf', '_checks']

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
		if remove[-1] in folder_contents:
			#print(folder_contents)
			for x in remove:
				if x in folder_contents:
					folder_contents.remove(x)
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
			state = file_list[0].lower()
			if state == 'california':
				file_list.pop(1)
				file_list.pop(3)
			
			county = file_list[2]
			year = file_list[1][2]		
			file_num = file_list[3]

			new_dir = output_path 
			for i in [state, file_list[1]]:
				new_dir = new_dir + "\\" + i
				if os.path.isdir(new_dir) == False:
					os.makedirs(new_dir)

			#Maine also has quirks
			if state == 'maine':
				file_num = file_list[-1]

			#This is important -- all the file numbers are the same for a county, year file, only the number after "-" is different
			if '-' in file_num:
				file_num_final = file_num.split("-")
			else:
				file_num_final = file_num
			
			file = "_".join([states[state], year, county, file_num_final[1]])
			new_path = new_dir + "\\" + file

			#this is to do regeneration as needed
			if regenerate:
				#print('regenerating')
				bad_cut(old_path, new_path, file, state, file_list[1], bad_cut_list, empty_list, "_A")
				continue


			#11/21/16 DO NOT COMMENT OUT; Just for NE 1880; since usually splitting method won't work for these, will have to make 
			# a specific splitting method in Prep_data_entry():
			if states[state] == 'NE' and year == '8':
				img = Image.open(old_path)
				file_path, filetype = os.path.splitext(new_path)
				width, height  = img.size
				width1 = int(width * .3) #width1 = int(width * .325)
				width2 = int(width * .85) #width2 = int(width * .85)
				if os.path.isfile(file_path + "_A" + '.jpg') == False:
					img.crop((width1, 0, width2, height)).save(file_path + "_A" + '.jpg')
				continue
			#11/21/16 Just want NE 1880; commenting out format_img
			
			#11/28/16 Just want to redo NE 1870
			#if states[state] == 'NE' and year == '7':
				#format_img(old_path, new_path)
			

			#11/29/16 Just want to redo IA 1880 real quick
			#if states[state] == 'IA' and year == '8':
				#format_img(old_path, new_path)
			
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


def read_metadata(metadata_csv):
	bad_cut_list = []
	empty_list = []
	bad_cut = 5
	empty = 6
	file = 2
	if metadata_csv == []:
		return [], []
	if 'xlsx' in metadata_csv:
		workbook = xlrd.open_workbook(metadata_csv)
		sheet = workbook.sheet_by_name('Sheet1')
		filename, filetype = os.path.splitext(metadata_csv)
		metadata_csv = open(filename + '.csv', "wb")
		writer = csv.writer(metadata_csv)
		for row in list(range(sheet.nrows)):
			writer.writerow(sheet.row_values(row))
		metadata_csv.close()
		metadata_csv = filename + '.csv'

	with open(metadata_csv, 'rt') as f:
		rows = csv.reader(f)
		rows.next()
		for row in rows:
			if row[bad_cut] == '1':
				bad_cut_list.append(row[file])
			if row[empty] != "":
				empty_list.append(row[file])
	return bad_cut_list, empty_list




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


	# each of the state-year csv's have idiosyncracies. I sacrifice efficiency for accuracy by making
	# a sub-function for each csv in ancestry that really needs it
	if states[state] == 'IA' and year == '1880':
		#no resplitting is needed, but we still have to mark in the csv documents that are blank
		pass

	if states[state] == 'NE' and year == '1870':
		#if both files are marked as bad cut I assume I need to regenerate them completely
		if new_file1 in bad_cut_list and new_file2 in bad_cut_list:
			#this is the only instance i can find where the cutting actually didn't work; file actually should not be split
			if 'Hall' in filename and '00390' in filename:
				for i in [(new_file1, new_file1_stamped), (new_file2, new_file2_stamped)]:
					if os.path.isfile(transfer_path[0] + "\\" + i[1]):
						os.remove(transfer_path[0] + "\\" + i[1])
				img = Image.open(old_path)
				for j in [new_path, regenerate_path]:
					file_path, filetype = os.path.splitext(j)
					if os.path.isfile(file_path + "_A" + '.jpg') == False:
						img.save(file_path + "_A" + '.jpg')
			else:
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
	if states[state] == 'NE' and year == '1880':
		#easier to not reas the csv
			if bad_cut_list == []:
			#no files were split for NE '1880', so can just stick to new_file0
			#these are the specific files that were cut incorrectly
				for exception in ['NE_8_Buffalo_00034', 'NE_8_Dodge_00139', 'NE_8_Howard_00274', 'NE_8_York_00006', 'NE_8_York_00007']:
					# no splitting was done in this folder, so I can just use new_file0. Vansh, who collected the data, said he could get the data on these,
					# so I don't need to add them to the regenerate folder
					if exception in new_file0_stamped:
						if os.path.isfile(transfer_path[0] + "\\" + new_file0_stamped):
							os.remove(transfer_path[0] + "\\" + new_file0_stamped)
							print(transfer_path[0] + "\\" + new_file0_stamped)
						img = Image.open(old_path)
				
						
						print(transfer_path[0] + "\\" + new_file0_stamped)
						width, height  = img.size
						new_width = .35 * width
						if width > height:
							img.crop((int(new_width),0, width, height)).save(transfer_path[0] + "\\" + new_file0_stamped)
						else:
							img.save(transfer_path[0] + "\\" + new_file0_stamped)
						break
					#os.remove(transfer_path[0] + "\\" + i[1])

	
			#here I assume for NE 1870 that if only one half is marked bad cut, this means that the first or second half is white space, and thus I can 
			# mark in the CSV which is a white space in the update metadata csv function. No resplitting is needed
		#elif new_file1 in bad_cut_list or new_file2 in bad_cut_list:
			

			#for i in [(new_file1, new_file1_stamped), (new_file2, new_file2_stamped)]:
				#bad_cut_list.remove(i[0])
				#delete file from output folder
				#if os.path.isfile(transfer_path[0] + "\\" + i[1]):
					#os.remove(transfer_path[0] + "\\" + i[1])
				#if i[0]
			#we take the old file, and now we want to convert it to jpeg, output it to both the output folder and the regenerate folder,
			# all without splitting it
			#for output_folder in [new_path, regenerate_path]:
				#img = Image.open(old_path)
				#filename, filetype = os.path.splitext(output_folder)
				#if os.path.isfile(filename + underscore_stamp + '.jpg') == False:
					#img.save(filename + underscore_stamp + '.jpg')


		################################################################################ will go into update_metadata function ############################################
	'''
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
def csv_metadata(metadata_xlsx, csv_name_output, dictionary, state, year):
	'''
	This function will take the metadata csv the undergrads made, and use it to make a master renaming csv.
	This new csv will include a new name for each file. I guess dictionary will only be needed when we actually rename the file
	'''
	new_csv_list = []
	if os.path.isdir(csv_name_output + "\\" + 'temp_csvs') == False:
		os.makedirs(csv_name_output + "\\" + 'temp_csvs')
	if 'xlsx' in metadata_xlsx:
		workbook = xlrd.open_workbook(metadata_xlsx)
		sheet = workbook.sheet_by_name('Sheet1')
		
		metadata_csv = open(csv_name_output + "\\" + 'temp_csvs' + "\\" + state + "_" + year + '.csv', "wb")
		writer = csv.writer(metadata_csv)
		for row in list(range(sheet.nrows)):
			#print(sheet.row_values(row))
			writer.writerow(sheet.row_values(row))
		metadata_csv.close()
	else:
		shutil.copy(metadata_xlsx, csv_name_output + "\\"+ "temp_csvs" + "\\" + state + "_" + year + '.csv')
	#print(metadata_csv)
	with open(csv_name_output + "\\" + 'temp_csvs' + "\\" + state + "_" + year + '.csv', 'rt') as f:
		file = csv.reader(f)
		file.next()
		for row in file:
			#print(row)
			new_year, old_file, new_county, bad_cut_indicator, empty_indicator = row[1], row[2], row[3], row[5], row[6]
			schedule, page_no,  establishment_count, legibility = row[7], row[8] ,row[9], row[10]
			
			notes = row[12]
			worse_version = ""
			duplicate = ""
			crossed_out = ""
			unusual_file = ""
			no_data_file = ""
			
			whitespace_file = ""
			information_not_attainable = ""
			
			old_name, old_type = os.path.splitext(old_file)
			#the old filenames have to match the ones in the actual directory -- the ones in the directory have labels, those in the csv do not
			if "_A" not in old_file:
				old_file = old_name + "_A" + old_type

			#in this case, at least for Iowa, we have a duplicate file e.g. 
			# IA_5_Jefferson_00023_1half.jpg vs IA_5_Jefferson_00023_2_1half.jpg
			
			#handle Iowa
			if state == "IA":
				#handle duplicates	#see dodumentation -- all collectors used "same or duplicate"
				if 'same' in notes.lower() or 'duplicate' in notes.lower():
					duplicate = "1"
				#handle no data or whitespace
				if empty_indicator != "":
					#same collector for these years
					if year == "1850" or year == "1860":
						if 'no data' in empty_indicator.lower():
							no_data_file = '1'
						if 'no text' in empty_indicator.lower():
							whitespace_file = '1'
					if year == "1870" or year == '1880':
						no_data_file = '1'
					#the one bad cut in IA 1880 -- the lst half is whitespace
					if 'IA_8_Jackson_00464' in old_file:
						empty_indicator = '1'
				#some bizarre markings here
				if year == '1880' and notes != "":
					#irregular files I treat as nullified by census taker
					for i in ['transferred', 'copied', 'omit', 'schedule', 'crossed out']:
						if i in notes.lower():
							crossed_out = '1'
							break
			# handle Nebraska -- lots of idiosyncracies here...
			if state == 'NE':
				#collector got a little enthusiastic with bad cut indicator....
				if year == '1860':
					if 'duplicate' in notes.lower():
						duplicate = '1'
					if empty_indicator != "":
						no_data_file = '1'

				if year == '1870':
					#the only file that is actually badly cut
					if bad_cut_indicator != "" and 'NE_7_Hall_00390' not in old_file:
						whitespace_file = '1'
					if 'cut off' in notes.lower() or 'county name is completely different' in notes.lower():
						information_not_attainable = '1'
					if 'same' in notes.lower() or 'duplicate' in notes.lower():
						#print(notes.lower())
						duplicate = '1'
					if empty_indicator != "":
						no_data_file = '1'

				if year == '1880':
					# NE 8 no longer split so I will skip every one with '2half'
					if '2half' in old_file:
						continue
					else: 
						filename_8, filetype_8 = os.path.splitext(old_file)
						meta_8 = filename_8.split("_")
						if '1half' in meta_8:
							meta_8.remove('1half')
						old_file = "_".join(meta_8) + filetype_8

			#for filename, some of them might have really long numbers, and extra counties if "-" condition not met
			filename, filetype = os.path.splitext(old_file)
			meta = filename.split("_")
			# sort of awkward, but best I can do right now to be accurate
			'''
			if '1half_A' in old_file:
				file_num = meta[-3][:6]
				tail = '1half_A.jpg'
			elif '2half_A' in old_file:
				file_num = meta[-3][:6]
				tail = '2half_A.jpg'
			elif '1half' in old_file:
				#take the first 6 numbers of this file number, like "NE_8_Cass_MileGrove_31641_217936_1half.jpg"
				file_num = meta[-2][:6]
				#print(filenum)
				tail = '1half_A.jpg'
			elif '2half' in old_file:
				file_num = meta[-2][:6]
				tail = '2half_A.jpg'
			elif "_A" in old_file:
				file_num = meta[-2][:6]
				tail = "A.jpg"
			else:
				file_num = meta[-1][:6]
				tail = 'A.jpg'
			'''
			file_num = meta[3][:6]
			# weird cases like NE_8_Cass_MileGrove_31641_217936_1half.jpg. But some duplicate files get caught in this condition sometimes
			if len(meta) == 7 and duplicate == "":
				file_num = meta[4][:6]
			

			if '1half' in old_file:
				tail = '1half_A.jpg'
			elif '2half' in old_file:
				tail = '2half_A.jpg'
			else:
				tail = "A.jpg"
			#For now, I will just use "A" instead of Source...
			#print([state, new_year[2], new_county.lower(), file_num, tail])
			new_file = "_".join([state, new_year[2], new_county.lower(), file_num, tail])
			new_csv_list.append([old_file, new_file, no_data_file, whitespace_file ,unusual_file, worse_version, duplicate, crossed_out ,schedule, page_no,establishment_count, legibility ,information_not_attainable])
	if os.path.isdir(csv_name_output + "\\" + state) == False:
		os.makedirs(csv_name_output + "\\" + state)
	with open(csv_name_output + "\\" + state + "\\" + year + '.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['old_file','new_file', 'no_data', 'whitespace' ,'unusual_file', 'worse_version', 'duplicate', 'Nullified/Crossed_Out', 'schedule', 'page_no','establishment_count', 'legibility','info_not_attainable'])
		for row in new_csv_list:
			writer.writerow(row)

	

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

####################################################csv_write and csv_dict have been moved to general code###################################################################


######################################################################
if __name__ == '__main__':
	folder_contents = os.listdir(csv_name_output)
	for i in range(len(folder_contents)):
		if os.path.isfile(csv_name_output + "\\" +folder_contents[i]):
			name = folder_contents[i].split("_")
			state_abbrev = name[0]
			year = '18' + name[1] + '0'
			csv_metadata(csv_name_output + "\\" +folder_contents[i], csv_name_output, {}, state_abbrev, year)

	#dictionary = collect(input_path)
	#print(list(dictionary.keys()))
	#bad_cut_list, empty_list = read_metadata([])
	#print(bad_cut_list)
	#print(empty_list)
	#populate(dictionary, input_path, True, bad_cut_list, empty_list)
	






