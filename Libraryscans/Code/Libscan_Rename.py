# exec(open("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Code\\Libscan_Rename.py").read()) 
import os, shutil, datetime, csv
import xlrd
#import ghostscript
#from wand.image import Image
from PIL import Image

one_slice = .4
two_slice = .6
threshold = .08

#input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Input\\Scans_via_Library_copy"
input_path_1 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\raw_data_copies\\Scans_via_Library_tiff\\Digital Scanning 5029-3"
input_path_2 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\raw_data_copies\\Scans_via_Library_tiff\\Digital Scanning 5029-6"
input_path_3 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\raw_data_copies\\Scans_via_Library_tiff\\Reels 132-149"
input_path_4 = "D:\\temp_nondropbox\\temp_raw_copies_tiff\\Digital Scanning 052017 TIFF"
input_path_5 = "D:\\temp_nondropbox\\temp_raw_copies_pdf"
#temporarily, I am not integrating KS 1880 with rest of libscans b/c syncing issues
input_KS_8 = "D:\\temp_nondropbox\\Adam\\Kansas 1880 (LibScans)\\Input"

input_path_list = [input_path_1, input_path_2, input_path_3]
#NOTE: Jeremy Rolls in input folder, I deleted not for dir issue, and turned Kanasas territory into Kansas
excel_path_1 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Temp\\Jeremy rolls_edited.xlsx"
#excel_path_2 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Temp\\jeremy_rolls_batch_2_edited.xlsx"
excel_path_3 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Temp\\batch3_edited.xlsx"
excel_path_4 = "D:\\temp_nondropbox\\New_batches_csv.xlsx"
excel_path_KS_8 = "D:\\temp_nondropbox\\Adam\\Kansas 1880 (LibScans)\\Kansas 1880.xlsx"

excel_path_list = [excel_path_1, excel_path_1, excel_path_3]

#output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output"
csv_name_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Renaming metadata"
#output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_tiff"
output_path = "D:\\temp_nondropbox\\Additional Output"
#just for Kansas 1880
#output_path = "D:\\temp_nondropbox\\Adam\\Kansas 1880 (LibScans)\\KS 1880 Output"
#for the new batch of libscans we just got, putting in non-dropbox

#output_path = "D:\\temp_nondropbox\\Additional Output"

temp_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Temp"

test_input = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Input\\Scans_via_Library_copy\\Batch_1\\batch 1 pdf"

states = {'california': 'CA', 'alabama': 'AL', 'arkansas': 'AR', 'colorado': 'CO','connecticut': 'CT', 'delaware': 'DE', 'dc': 'dc', 'florida': 'FL', 'georgia':'GA', 'kentucky': 'KY', 
'idaho territory': 'ID' ,'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas':'KS', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD', 'massachusetts': 'MA', 'michigan': 'MI', 
'minnesota': 'MN', 'mississippi': 'MS', 'montana': 'MT','nebraska':'NE', 'new hampshire': 'NH', 'new jersey': 'NJ','new mexico':'NM' ,'new york':'NY', 'north carolina':'NC', 'ohio':'OH',
'oregon': 'OR','pennsylvania' : 'PA', 'south carolina': 'SC', 'tennessee': 'TN', 'texas': 'TX','utah':'UT' ,'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV', 
'wisconsin': 'WI'}

remove = ['.dropbox', 'desktop.ini', 'Thumbs.db']
no_excel = ['.xls', '.xlsx']
not_for_dir = ['?']

def collect(input_path):
	#print(input_path)
	#base case
	if os.path.isdir(input_path) == False:
		x = 'root'
		#print(x)
		return x
	#recursive case
	else:
		folder_contents = os.listdir(input_path)
		if remove[0] in folder_contents:
			folder_contents = [folder_contents.remove(x) for x in remove]
		#print(folder_contents)
		current_dictionary = {}
		for element in folder_contents:
			#print(element)
			element_strip, element_type = os.path.splitext(input_path + "\\" + element)
			
			if element_type not in no_excel:
				current_path = input_path + "\\" + element
				lower_dictionary = collect(current_path)
				#print(current_path)
				#if lower_dictionary == 'root':
				current_dictionary[element] = lower_dictionary
					#print(element)
		return current_dictionary


def get_info(old_dictionary, current_path, new_dictionary):
	#print(old_dictionary)
	keys = list(old_dictionary.keys())
	#print(keys)
	if 'root' in list(old_dictionary.values()):
		for key in keys:
			#print(key)
			#Roll 17 PDF folder in rework batch folder - not sure why it exists; that's why the line is needed
			#if os.path.isdir(current_path + "\\" + key) == False:
				#print(key, 'path:', current_path + "\\" + key)
			old_path = current_path + "\\" + key
			if os.path.isdir(old_path):
				print(old_path)
				next_path = old_path
				get_info(old_dictionary[key], next_path, new_dictionary)
				continue
				#take out Roll from file name
			if key == 'Thumbs.db' or key == 'Reel 5_000295.tif' or key == 'Reel 5_000296.tif': #corrupted CA files in roll 5
				continue
			if "Roll" in key:
				decomp = key.split('Roll', 1)[1]
			else:
				#if key == 'DSI Invoice 5301 Inventory.pdf':
					#continue
				#print(key)
				decomp = key.split('Reel ', 1)[1]
			decomp2 = decomp.split('_')
				#print(decomp2)
			roll_num = decomp2[0]
				#take out the type of file from the file number
				#file_num = decomp2[1].split(".")[0]
			file_num = decomp2[1]
				#print(file_num)
			need_zero = 4 - len(roll_num)
			roll_num = '0' * need_zero + roll_num
			#print(roll_num)
			if roll_num not in new_dictionary:
				new_dictionary[roll_num] = {}
			new_dictionary[roll_num][file_num] = old_path    
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			get_info(old_dictionary[key], next_path, new_dictionary)
		return new_dictionary


def populate(new_dictionary, excel_path, csv_sheet, skip_line):
	

	workbook = xlrd.open_workbook(excel_path)
	sheet = workbook.sheet_by_name(csv_sheet)
	#csv_file = open(temp_path + "\\" + 'Sheet1.csv', "w", newline = "") #originally wt, no newline para #apparently py 2.7 doesnt like this
	csv_file = open(temp_path + "\\" + csv_sheet + '.csv', "wb") #originally wt, no newline para
	writer = csv.writer(csv_file)

	for row in list(range(sheet.nrows)):
		#print(sheet.row_values(row))
		writer.writerow(sheet.row_values(row))
	csv_file.close()

	with open(temp_path + "\\" + csv_sheet + '.csv', 'rt') as f:
		file = csv.reader(f)
		#file.__next__() #apparently Py 2.7 doesnt like this
		for x in range(skip_line):
			#print('skipped')
			file.next()
		for row in file:
			#print(row)
			#print(row)
			#if row[0] == '':
			#print(row)
			if row == ['', '', '', '', '']:
				print('Process Complete')
				return
			if row[0] == '':
				continue
			roll_num, State, County, Date = int(float(row[0])), row[2].lower(), row[3], row[4]
			no_zero = 4 - len(str(roll_num))
			roll_num = '0'*no_zero + str(roll_num)
			#print(roll_num)
			#if State == 'kansas territory':
				#State = 'kansas'
			Date = Date.split(".")[0]

			#dir_list = [State, Date, County]
			dir_list = [State, Date]
			#for i in range(len(dir_list)):
				#for j in not_for_dir:
					#if dir_list[i].endswith(j):
						#print(j)
						#dir_list[i] = 'Unknown'
			#new_dir = output_path
			
			#for i in dir_list:
				#new_dir = new_dir + "\\" + i 
				
				#if os.path.isdir(new_dir) == False:
					#try:
						#os.makedirs(new_dir)
					#except FileNotFoundError:
						#print("\nOh man, you have a file not found error (race condition)\n")
			
			if str(roll_num) in list(new_dictionary.keys()):
				#print(roll_num)
				keys = list(new_dictionary[str(roll_num)].keys())
				new_dir = output_path
				for i in dir_list:
					new_dir = new_dir + "\\" + i 
				
					if os.path.isdir(new_dir) == False:
						try:
							os.makedirs(new_dir)
						except FileNotFoundError:
							print("\nOh man, you have a file not found error (race condition)\n")
				for key in keys:
					old_path = new_dictionary[str(roll_num)][key]
					#print(old_path)
					new_path = new_dir + "\\" + "_".join([states[State], Date, County, key])
					#print('old path:\n', old_path, 'new_path\n', new_path)
					
					#shutil.copy(old_path, new_path)

					format_img(old_path, new_path)


def csv_metadata_2(metadata_xlsx, csv_name_output, dictionary, state, year):
	'''
	This function will replace csv_metadata below for creating the master renaming csv. So anything that is not a priority state
	with the expection of MN 1880 should be used with this new function
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
	# duplicates are usually not an issue for renaming, except in cases when the duplicate file's new name is the same as the non-duplicates new file
	duplicate_set = set([])
	with open(csv_name_output + "\\" + 'temp_csvs' + "\\" + state + "_" + year + '.csv', 'rt') as f:
		file = csv.reader(f)
		file.next()
		for row in file:
			new_year, old_file, new_county, RA = row[1], row[2], row[3], row[4]
			bad_cut, page_no, establishment_count, legibility, totals_inc, notes = row[5], row[6], row[7], row[8], row[9], row[10]
			multiple_counties, no_data, crossed, schedule, duplicate, variant = row[11], row[12], row[13], row[14], row[15], row[16]

			#new_county may have a back slash -- this is bad for renaming procedure
			if "/" in new_county:
				new_county_parts = new_county.split("/")
				new_county = "-".join(new_county_parts)

			old_name, old_type = os.path.splitext(old_file)
			#the old filenames have to match the ones in the actual directory -- the ones in the directory have labels, those in the csv do not
			if "_L." not in old_file:
				old_file = old_name + "_L" + old_type

			#this is the only one that is necessary. For duplicates, multiple counties, variant, no data, and rest of nullified, they are already
			#marked in the csv. Those marks will be used in the filtering phase, but not here
			if 'cross' in notes or 'void' in notes:
				crossed ='1'

			filename, filetype = os.path.splitext(old_file)
			meta = filename.split("_")
			file_num = meta[3][-5:]

			if '1half' in old_file:
				#tail = '1half_L.jpg'
				tail = 'l_L.jpg'
			elif '2half' in old_file:
				#tail = '2half_L.jpg'
				tail = 'r_L.jpg'
			else:
				tail = "L.jpg"

			new_file = "_".join([state, new_year[2], new_county.lower(), file_num, tail])
			if duplicate == '1' and new_file in duplicate_set:
				dup_file, dup_type = os.path.splitext(new_file)
				dup_count = meta[4]
				new_file = dup_file + "_Dup" + dup_count + dup_type
			else:
				duplicate_set.add(new_file)
			new_csv_list.append([old_file, new_file, state, year, new_county, RA, bad_cut, page_no, establishment_count, legibility, totals_inc, notes,
				multiple_counties, no_data, crossed, schedule, duplicate, variant])
	if os.path.isdir(csv_name_output + "\\" + state) == False:
		os.makedirs(csv_name_output + "\\" + state)
	with open(csv_name_output + "\\" + state + "\\" + state + '_' + year + '.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['old_file','new_file', 'state', 'year' ,'county', 'RA', 'bad_cut', 'page_no', 'estab_count', 'legibility', 'totals_inc', 
					'notes','multiple_counties', 'no_data', 'crossed', 'schedule', 'duplicate', 'variant'])
		for row in new_csv_list:
			writer.writerow(row)




























def csv_metadata(metadata_xlsx, csv_name_output, dictionary, state, year):
	'''
	This function will take the metadata csv the undergrads made, and use it to make a master renaming csv.
	This new csv will include a new name for each file. I guess dictionary will only be needed when we actually rename the file. For year, it needs to be 
	# 4 digit year, so name the metadata input files as 1 number for a year e.g if year is 1860 for NE, looks like NE_6_...
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
	# duplicates are usually not an issue for renaming, except in cases when the duplicate file's new name is the same as the non-duplicates new file
	duplicate_set = set([])
	with open(csv_name_output + "\\" + 'temp_csvs' + "\\" + state + "_" + year + '.csv', 'rt') as f:
		file = csv.reader(f)
		file.next()
		for row in file:
			new_year, old_file, new_county, bad_cut_indicator, empty_indicator = row[1], row[2], row[3], row[5], row[6]
			schedule, page_no,  establishment_count, legibility = row[7], row[8] ,row[9], row[10]
			
			#new_county may have a back slash -- this is bad for renaming procedure
			if "/" in new_county:
				new_county_parts = new_county.split("/")
				new_county = "-".join(new_county_parts)

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
			if "_L." not in old_file:
				old_file = old_name + "_L" + old_type

			#handle Kansas
			if state == 'KS':
				if empty_indicator != "":
					if 'no data' in empty_indicator.lower():
						no_data_file = '1'
					if 'no text' in empty_indicator.lower():
						whitespace_file = '1'
				if year == '1870' or '1880':
					if 'duplicate' in notes.lower():
						duplicate = '1'
					if 'duplication of previous photo' in notes.lower():
						worse_version = '1'
					if 'cross' in notes.lower():
						crossed_out = '1'
					if 'no county name' in notes.lower():
						information_not_attainable = '1'
			#Minnosota
			if state == 'MN' and year == '1860':
				if notes != "":
					for i in ['county name not legible', 'too dark', 'county name illegible']:
						if i in notes.lower():
							information_not_attainable = '1'
				if 'no data' in empty_indicator.lower():
					no_data_file = '1'
				#these files are corrupted
				for i in ['156', '240', '269', '284', '350', '355', '406', '430', '434', '452']:
					if i in old_file:
						information_not_attainable = '1'

			if state == 'MN' and year == '1850':
				# only 4 files that are actually manufacturing census
				if '296' in old_file: 
					duplicate = '1'
				if '277' in old_file:
					worse_version = '1'

				if 'no data' in empty_indicator.lower():
					no_data_file = '1'
				elif 'no text' in empty_indicator.lower():
						whitespace_file = '1'
				else:
					no_data_count = 1
					for i in ['159', '277', '296', '453']:
						if i in old_file:
							#print(old_file)
							no_data_count = 0
							break
					#these are the only 4 files with data, so if a file isn't one, mark as no data
					if no_data_count == 1:
						no_data_file = '1'


			#for filename, some of them might have really long numbers, and extra counties if "-" condition not met
			filename, filetype = os.path.splitext(old_file)
			meta = filename.split("_")
			#we want the last 5 digits (lots of leading zeros in old filenum)
			#file_num = meta[3][:6]
			file_num = meta[3][-5:]
			#no county in old filename for this state-year
			if state == 'MN' and year == '1850':
				file_num = meta[2][:6]

			if '1half' in old_file:
				#tail = '1half_L.jpg'
				tail = 'l_L.jpg'
			elif '2half' in old_file:
				#tail = '2half_L.jpg'
				tail = 'r_L.jpg'
			else:
				tail = "L.jpg"
			# for Libscan, old files already have labels "_L"
			
			'''
			if '1half' in old_file:
				#take the first 6 numbers of this file number
				filenum = meta[-3][:6]
				print(filenum)
				tail = '1half_L.jpg'
			elif '2half' in old_file:
				filenum = meta[-3][:6]
				tail = '2half_L.jpg'
			else:
				file_num = meta[-2][:6]
				tail = 'L.jpg'
			
			'''
			#For now, I will just use "A" instead of Source...
			new_file = "_".join([state, new_year[2], new_county.lower(), file_num, tail])
			# duplicate issue (see line above largest for loop)
			if duplicate == '1' and new_file in duplicate_set:
				dup_file, dup_type = os.path.splitext(new_file)
				dup_count = meta[4]
				new_file = dup_file + "_Dup" + dup_count + dup_type
			else:
				duplicate_set.add(new_file)
			new_csv_list.append([old_file, new_file, no_data_file, whitespace_file ,unusual_file, worse_version, duplicate, crossed_out ,schedule, page_no ,establishment_count, legibility ,information_not_attainable])
	if os.path.isdir(csv_name_output + "\\" + state) == False:
		os.makedirs(csv_name_output + "\\" + state)
	with open(csv_name_output + "\\" + state + "\\" + year + '.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['old_file','new_file', 'no_data', 'whitespace' ,'unusual_file', 'worse_version', 'duplicate', 'Nullified/Crossed_Out', 'schedule', 'page_no', 'establishment_count', 'legibility','info_not_attainable'])
		for row in new_csv_list:
			writer.writerow(row)




def format_img(old_path, new_path):
	#print(new_path)
	img = Image.open(old_path)
	width, height  = img.size
	#if '170' not in old_path and 'WI' in new_path:
		#img_rotate = img.rotate(-90, expand=True)
		#file_path, filetype = os.path.splitext(new_path)
		#if os.path.isfile(file_path + "_L" + '.jpg') == False:
			#img_rotate.save(file_path + "_L" + '.jpg')

	#elif old_path == 'test':
	if width > height and abs(float(width - height))/float(height) > threshold:
		transfer_path = new_path.rsplit("\\", 1)
		filename, filetype = os.path.splitext(transfer_path[1])

		width_one = one_slice * width
		width_two = two_slice * width
		image_one, image_two = img, img
		if os.path.isfile(transfer_path[0] + "\\" + filename + '_' + '2half' + "_L" + '.jpg') == False:
			image_one.crop((int(width_one), 0, width, height)).save(transfer_path[0] + "\\" + filename + '_' + '2half' + "_L" + '.jpg')
			image_two.crop((0, 0, int(width_two), height)).save(transfer_path[0] + "\\" + filename + '_' + '1half' + "_L" + '.jpg')
	#elif 'WI' in new_path:
	else: 
		file_path, filetype = os.path.splitext(new_path)
		if os.path.isfile(file_path + "_L" + '.jpg') == False:
			img.save(file_path + "_L" + '.jpg')

'''
#only used for PDF conversions

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
			if os.path.isfile(transfer_path[0] + "\\" + filename + '_' + '2half' +  "_L" + '.jpg') == False:
				image_one.save(filename = transfer_path[0] + "\\" + filename + '_' + '2half' + "_L" +'.jpg') #we need to check save also take path, not just filename
				image_two.save(filename = transfer_path[0] + "\\" + filename + '_' + '1half' + "_L" + '.jpg')
		else:
			#img.format = 'jpeg'
			img.compression_quality = 99
			file_path, filetype = os.path.splitext(new_path)
			if os.path.isfile(file_path + "_L" +'.jpg') == False:
				img.save(filename = file_path + "_L" +'.jpg')
			#shutil.copy(old_path, new_path)
'''
####################################################csv_write and csv_dict have been moved to general code###################################################################
'''
def csv_write(dictionary, package_path):
	keys = list(dictionary.keys())
	for tup in keys:
		csv_list = dictionary[tup]
		filename = package_path + "\\" + 'Ancestry' + "\\" + tup[0] + "\\" + tup[1]
		os.makedirs(filename)
		with open(filename + "\\" + 'Package.csv', 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(['County', 'File Number', 'Current Location'])
			for row in csv_list:
				#with open(filename, 'w', newline = '') as f: # Python 2.7 complains with new line arg
				#writer.writerow(['File Name', 'Current path', 'County (if given)'])
				writer.writerow(row)


def csv_dict(current_path, package_path, dictionary):
	if os.path.isdir(current_path) == False: 
		rel_path = os.path.relpath(current_path, output_path) # output_path is a global variable 
		split = rel_path.split("\\")
		state, year, county, file_num = split[0], split[1], split[2], split[3]
		meta = [county, file_num, current_path]

		if (state, year) not in dictionary:
			dictionary[(state, year)] = []
		dictionary[(state, year)].append(meta)
	else:
		folder_contents = os.listdir(current_path)
		for element in folder_contents:
			next_path = current_path + "\\" + element
			csv_dict(next_path, package_path, dictionary)
		return dictionary

'''

######################################################################
if __name__ == '__main__':
	#csv_metadata(csv_name_output + "\\" +"MN_5_L_metadata_edited.csv", csv_name_output, {}, 'MN', '1850')



	dictionary = collect(input_path_4)
	new_dictionary = get_info(dictionary, input_path_4, {})
	populate(new_dictionary, excel_path_4, 'Sheet1', 1)
	

	'''
	folder_contents = os.listdir(csv_name_output)
	for i in range(len(folder_contents)):
		#if os.path.isfile(csv_name_output + "\\" +folder_contents[i]) and '5' not in folder_contents[i]:
		#if os.path.isfile(csv_name_output + "\\" +folder_contents[i]) and 'edited' in folder_contents[i]:
		#print(folder_contents[i])
		if folder_contents[i] in ['NH_1870_L_metadata_edited.csv', 'NY_1850_L_metadata_edited.csv', 'MI_1850_L_metadata_edited.csv', 'VA_1860_L_metadata_edited.csv']:
			
			name = folder_contents[i].split("_")
			state_abbrev = name[0]
			if len(name[1]) == 1:
				year = '18' + name[1] + '0'
			elif len(name[1]) == 4:
				year = name[1]
			csv_metadata_2(csv_name_output + "\\" +folder_contents[i], csv_name_output, {}, state_abbrev, year)
	'''
	
	#just for KS 1880
	#dictionary = collect(input_KS_8)
	#new_dictionary = get_info(dictionary, input_KS_8, {})
	#populate(new_dictionary, excel_path_KS_8, 'Sheet1', 1)



	#Just for KS 1880

	'''
	#for i in range(len(input_path_list)):
	dictionary = collect(input_path_list[2])
	#print(dictionary)
	new_dictionary = get_info(dictionary, input_path_list[2], {})
	#print(dictionary, new_dictionary)
	populate(new_dictionary, excel_path_list[2], 'Sheet1', 1)
	#populate(new_dictionary, excel_path_2, 'Sheet1', 3)
	'''

