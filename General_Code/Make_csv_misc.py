import os, shutil, datetime, sys
import csv, wand

#from wand.image import Image 
from PIL import Image

shrink_factor = .2
quality_factor = 65

ancestry_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output"
ancestry_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output_final"

MO_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Output"
MO_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Output_final"

lib_scan_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output"
lib_scan_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_final"
lib_scan_output_tiff = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_tiff"
KS_1880_output = "D:\\temp_nondropbox\\Adam\\Kansas 1880 (LibScans)\\KS 1880 Output"
IA_1880_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output_final\\iowa\\1880"
#MN_1850 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_pdf_incomplete\\minnesota"
NH_rename_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_tiff\\new hampshire\\1870_rename"
Famsearch_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Output_final"
Nara_texas_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Nara_texas\\Output"

test = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Make_csv_rename_test"
package_test = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_tiff\\alabama"

package_folder = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\metadata_collection"
#package_folder = "D:\\temp_nondropbox\\Adam\\Iowa 1880 (Ancestry) Regen\\Package"

remove = ['desktop.ini', '.dropbox']
output_path_list = [ancestry_output, MO_output, lib_scan_output]
output_path_final_list = [ancestry_output_final, MO_output_final, lib_scan_output_final]
package_list = ['Ancestry', 'MO', 'Library_Scans']
file_stamp = ['A', 'S', 'L']

states = {'california': 'CA', 'alabama': 'AL', 'arkansas': 'AR', 'colorado': 'CO','connecticut': 'CT', 'delaware': 'DE', 'dc': 'dc', 'florida': 'FL', 'georgia':'GA', 'kentucky': 'KY', 
'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas':'KS', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD', 'massachusetts': 'MA', 'michigan': 'MI', 
'minnesota': 'MN', 'mississippi': 'MS', 'montana': 'MT','nebraska':'NE', 'new hampshire': 'NH', 'new jersey': 'NJ', 'new york':'NY', 'north carolina':'NC', 'ohio':'OH', 
'pennsylvania' : 'PA', 'south carolina': 'SC', 'tennessee': 'TN', 'texas': 'TX', 'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV', 
'wisconsin': 'WI'}

#csv_header = ['State', 'Year', 'File', 'County', 'RA_name', 'bad_cut', 'empty', 'Schedule', 'page_no', 'estab_count', 'legibility', 'totals_incl', 'Notes']
csv_header = ['State', 'Year', 'File', 'County', 'RA_name', 'bad_cut', 'no data', 'Schedule', 'page_no', 'estab_count', 'legibility', 'totals_incl', 'Notes', 'whitespace',
			   'duplicate', 'nullified/crossed out', 'info not attainable']



def csv_write(dictionary, package_folder, stamp):
	'''
	This function takes a dictionary from csv_dict function, a desired output
	folder in the metadata collection folder, and a stamp, which is a letter code indicating
	the source of the files
	'''

	keys = list(dictionary.keys())
	#print(keys)
	for tup in keys:
		state, year = tup[0], tup[1]
		#print(state, year)
		csv_list = dictionary[tup]
		csv_folder = package_folder + "\\" + 'Csv_Folder'
		
		if os.path.isdir(csv_folder) == False:
			os.makedirs(csv_folder)
		csv_file = csv_folder + "\\" + "_".join([state, year, stamp, 'metadata.csv'])
		#print('hey!',csv_folder)
		#print(csv_file, state)
		if os.path.isfile(csv_file):
			os.remove(csv_file)
		with open(csv_file, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(csv_header)
			for row in csv_list:
				#print(row)
				#with open(filename, 'w', newline = '') as f: # Python 2.7 complains with new line arg
				#writer.writerow(['File Name', 'Current path', 'County (if given)'])
				writer.writerow(row)


def csv_dict(current_path, output_path, dictionary):
	'''
	This function takes a year-state folder with files, which is intended to be
	packaged into the metadata collection folder. Note that current path and output path are the same folder,
	when the function is called initially. Dictionary is an empty dictionary
	'''
	

	if os.path.isdir(current_path) == False: 
		#print(current_path)
		#just Nara
		rel_path = os.path.relpath(current_path, output_path) # output_path is a global variable 
		#state = 'TX'
		#year = '8'
		#meta = [state, year, rel_path]
			#
		#if state != 'Csv':
			#if (state, year) not in dictionary:
				#dictionary[(state, year)] = []
			#dictionary[(state, year)].append(meta)
		#just Nara
		
		#print(rel_path)
		split = rel_path.split("_")
		#print(split)
		if len(split) <= 2:
			pass
		else:
			if len(split) == 3:
				state, year, file_num = split[0], split[1], split[2]
				meta = [state, year, file_num]
				#print(meta)
			elif len(split) >= 4:
				state, year, county = split[0], split[1], split[2]
				meta = [state, year, rel_path, county]

				#print(meta)
			
			
			if state != 'Csv':
				if (state, year) not in dictionary:
					dictionary[(state, year)] = []
				dictionary[(state, year)].append(meta)
				
	else:
		folder_contents = os.listdir(current_path)
		for element in folder_contents:
			next_path = current_path + "\\" + element
			csv_dict(next_path, output_path, dictionary)
		return dictionary


def rename(output_path, stamp):
	'''
	This function will "stamp" every file in the folder that is passed in as the output_path parameter.
	By stamp, I mean append a one letter code indicating the source of the file to the filename of every file
	'''

	if '.dropbox' in output_path or 'desktop.ini' in output_path:
		pass
	elif os.path.isdir(output_path) == False:
		filename, filetype = os.path.splitext(output_path)
		new_name = filename + "_" + stamp + filetype
		if os.path.isfile(new_name) and os.path.isfile(output_path):
			os.remove(output_path)
		elif filename.endswith("_" + stamp) == False:
			print('old: %s new: %s', output_path, new_name)
			os.rename(output_path, new_name)
	else: 
		folder_contents = os.listdir(output_path)
		for element in folder_contents:
			next_path = output_path + "\\" + element
			rename(next_path, stamp)

def rename_NH(input_path, county, year):
	files = os.listdir(input_path)
	for file in files:
		old_dir = input_path + "\\" + file
		#print(old_dir)
		meta = file.split("_")
		#print(meta)
		if len(meta) == 6:
			new_file = "_".join(['NH', year, county, meta[-3], meta[-2], meta[-1]])
		else:
			new_file = "_".join(['NH', year, county, meta[-2], meta[-1]])
		new_dir = input_path + "\\" + new_file
		#print(old_dir, new_dir, '\n')
		if old_dir != new_dir:
			os.rename(old_dir, new_dir)


# :( :( :(
def no_county_folder(current_path, input_path, output_path_final):
	if '.dropbox' in current_path or 'desktop' in current_path:
		pass
	elif os.path.isdir(current_path) == False:
		rel_path = os.path.relpath(current_path, input_path)
		meta = rel_path.split("\\")
		#print(meta)
		state, year, file = meta[0], meta[1], meta[-1]

		new_path = output_path_final
		for i in [state, year]:
			new_path = new_path + "\\" + i
			if os.path.isdir(new_path) == False:
					os.makedirs(new_path)

		new_path = new_path + "\\" + file
		if os.path.isfile(new_path) == False:
			#print(current_path)
			shutil.copy(current_path, new_path)
	else:
		folder_contents = os.listdir(current_path)
		for x in remove:
			if x in folder_contents:
				folder_contents.remove(x)
		for element in folder_contents:
			next_path = current_path + "\\" + element
			no_county_folder(next_path, input_path, output_path_final)

def rename_w_metadata(input_csv, input_folder):
	'''
	For now, this will take a processed renaming csv, and use it to rename a folder of files (input folder)
	'''
	
	with open(input_csv, 'rt') as f:
		file = csv.reader(f)
		file.next()
		for row in file:
			old_file, new_file = row[0], row[1]
			old_path = input_folder + "\\" + old_file
			#print(old_path)
			#break

			new_path = input_folder + "\\" + new_file
			#if duplicate != "" and os.path.isfile(new_path):
				#counter += 1
				#file, filetype = os.path.splitext(new_path)
				#new_path = file + "_Dup" + str(counter) + filetype
			#stamp = "_" + stamp
			#print(stamp)
			#return stamp
			#if stamp not in old_file:
				#file, filetype = os.path.splitext(old_path)
				#old_path = file + "_" + stamp + filetype
			if old_path != new_path and os.path.isfile(new_path) == False:
				#print(old_path, new_path)
				os.rename(old_path, new_path)
			'''
			if os.path.isfile(old_path) == False:
				print('old path:',old_path, "\n new path:", new_path)
				#os.rename(old_path, new_path)
			'''
			# test this condition first before commencing with os.rename above
			'''
			if os.path.isfile(old_path) == False:
				print(old_path)
			'''
		print("Done with", old_file)

def check_renamed_files(input_csv, input_folder, checking_folder_path, task):
	'''
	This function takes in the metadata collection sheets used to rename the files before shipment
	to data collection companies, along with the renamed file folders, and generated new folders with copied
	files that will be used to check if files are corrupted, duplicated, worse_version, etc. option3 will organize filtered files
	(filtered via final filter function) into sub-folders by schedule
	'''

	#just want the name of the csv, not it's path
	csv_file_decomp = input_csv.rsplit("\\", 1)
	csv_file_decomp = csv_file_decomp[1].split("_")
	print(csv_file_decomp)
	#print(input_csv)
	state, year = csv_file_decomp[0], csv_file_decomp[1][:-4]
	checking_st_yr_folder = checking_folder_path + "\\" + state + "\\" + year
	#print(checking_st_yr_folder)
	

	option1_names = ['no_data', 'whitespace', 'unusual_file', 'crossed', 'info_not_attainable']
	option2_names = ['worse_version', 'duplicate']

	if task == 'option1':
		for field in option1_names:
			for path in [checking_st_yr_folder, checking_st_yr_folder + "\\" + field, checking_st_yr_folder + "\\" + field + "\\" + 'False_Alarm']:
				if os.path.isdir(path) == False:
					os.makedirs(path)
	if task == 'option2':
		for field in option2_names:
			field_folder = checking_st_yr_folder + "\\" + field
			for path in [checking_st_yr_folder, field_folder, field_folder + "\\" + 'False_Alarm', field_folder + "\\" + 'Originals']:
				if os.path.isdir(path) == False:
					os.makedirs(path)
		#make dictionary
		checking_dict = {}
		
	
	#if task == 'option3':



	with open(input_csv, 'rt') as f:
		
		file = csv.reader(f)
		file.next()

		for row in file:
			
			new_file, no_data, whitespace, unusual_file = row[1], row[2], row[3], row[4]
			worse_version, duplicate, crossed, info_not_attainable = row[5], row[6], row[7], row[12]
			schedule, page_no, est_count, legibility = row[8], row[9], row[10], row[11]

			new_path = input_folder + "\\" + new_file

			option1 = [no_data, whitespace, unusual_file, crossed, info_not_attainable]
			option2 = [worse_version, duplicate]

			if task == 'option1':
				for i in range(len(option1)):
					if option1[i] == "1":
						shutil.copy(new_path, checking_st_yr_folder + "\\" + option1_names[i] + "\\" + new_file)

			if task == 'option2':
				for i in range(len(option2)):
					if option2[i] == '1' and os.path.isfile(checking_st_yr_folder + "\\" + option2_names[i] + "\\" + new_file) == False:
						shutil.copy(new_path, checking_st_yr_folder + "\\" + option2_names[i] + "\\" + new_file)
					if option2[i] == '2' and os.path.isfile(checking_st_yr_folder + "\\" + option2_names[i] + "\\" +  'Originals' + "\\" + new_file) == False:
						shutil.copy(new_path, checking_st_yr_folder + "\\" + option2_names[i] + "\\" +  'Originals' + "\\" + new_file)
				'''
				meta = new_file.split("_")
				state_abbrev, year, county, filenum = meta[0], meta[1], meta[2], meta[3]
				
				if county not in checking_dict:
					checking_dict[county] = []
				
				next_file = {'new_file': new_file ,'schedule': schedule, 'page_no': page_no, 'est_count': est_count, 'legibility': legibility, 
														'worse_version': worse_version, 'duplicate': duplicate}
				checking_dict[county].append(next_file)
				'''
	print("Done with %s_%s", state, year)


def rearrange_by_schedule(crosswalk_csv, metadata_csv_folder, renamed_file_input_folder, filtered_folder, not_there_folder ,output_folder):
	'''
	this function will only be for rearranging 1880 folders by schedule. Only do this AFTER running check_renamed_files() and then final_filter() on the files.
	crosswalk_csv will be the schedule cross walk Julius made. file_input_folder will be renamed files
	folder, or the filtered files folders. ouput folder path should be "D:\temp_nondropbox\Adam\Priority States 1880 - by schedule"
	'''
	crosswalk_dict = {}

	with open(crosswalk_csv, 'rt') as f:
		file = csv.reader(f)
		file.next()
		for row in file:
			meta = row[0].split("_")
			state, year = meta[0], meta[1]
			if (state, year) not in crosswalk_dict:
				crosswalk_dict[(state, year)] = {}
			#the file labels are not there for NE or for MO :<
			if 'NE' in row[0]:
				file, filetype = os.path.splitext(row[0])
				if '1half' in file:
					file_split = file.split('_1half')
					row[0] = file_split[0]+ "_A" + filetype
				else:
					row[0] = file + "_A" + filetype
				print(row[0])
			if 'MO' in row[0]:
				file, filetype = os.path.splitext(row[0])
				row[0] = file + "_S" + filetype
				#print(row[0])

			crosswalk_dict[(state, year)][row[0]] = row[1]
			#print(row[0], row[1])
	print(crosswalk_dict.keys())
	for state_year_key in crosswalk_dict.keys():
		if len(state_year_key[1]) == 1:
			state, year = state_year_key[0], '18' + state_year_key[1] + '0'
		else:
			state, year = state_year_key[0], state_year_key[1]

		metadata_csv = metadata_csv_folder + "\\" + state + "_" + year + ".csv"

		#print(metadata_csv)
		with open(metadata_csv, 'rt') as f:
			#if 'NE' in metadata_csv:
				#print(state_year_key)
				#print(crosswalk_dict[state_year_key].keys())
			file = csv.reader(f)
			file.next()
			for row in file:
				old_file, new_file = row[0], row[1]
				if old_file in crosswalk_dict[state_year_key]:
					#if 'NE' in metadata_csv or 'MO' in metadata_csv:
						#print('hey it worked')
					#if 'NE' in metadata_csv:
						#print(old_file)
					schedule = crosswalk_dict[state_year_key][old_file]

					regular_folder = output_folder + "\\" + 'Regular files' + "\\" + state + "\\" + year + "\\" + schedule
					filtered_cross_folder = output_folder + "\\" + 'Filter' + "\\" + state + "\\" + year + "\\" + 'crossed' + "\\" + schedule
					filtered_worsever_folder = output_folder + "\\" +  'Filter' + "\\" + state + "\\" + year + "\\" + 'worse_version' + "\\" + schedule
					otherwise_folder = not_there_folder + "\\" + state +  "\\" + year 
				
					for i in [regular_folder, filtered_cross_folder, filtered_worsever_folder, otherwise_folder]:
						if os.path.isdir(i) == False:
							os.makedirs(i)

					if os.path.isfile(renamed_file_input_folder + "\\" + state + "\\" + year + "\\" + new_file) and os.path.isfile(regular_folder + "\\" + new_file) == False:
						shutil.copy(renamed_file_input_folder + "\\" + state + "\\" + year + "\\" + new_file, regular_folder + "\\" + new_file)
					elif os.path.isfile(filtered_folder + "\\" + state + "\\" + year + "\\" + 'crossed' + "\\" + new_file) and os.path.isfile(filtered_cross_folder + "\\" + new_file) == False:
						shutil.copy(filtered_folder + "\\" + state + "\\" + year + "\\" + 'crossed' + "\\" + new_file, filtered_cross_folder + "\\" + new_file)
					elif os.path.isfile(filtered_folder + "\\" + state + "\\" + year + "\\" + 'worse_version' + "\\" + new_file) and os.path.isfile(filtered_worsever_folder + "\\" + new_file) == False:
						shutil.copy(filtered_folder + "\\" + state + "\\" + year + "\\" + 'worse_version' + "\\" + new_file, filtered_worsever_folder + "\\" + new_file)
					else:
						#print('RuhRoh Scooby! %s', new_file)
						pass
				else:
					if os.path.isfile(renamed_file_input_folder + "\\" + state + "\\" + year + "\\" + new_file) and os.path.isfile(otherwise_folder + "\\" + new_file) == False:
						shutil.copy(renamed_file_input_folder + "\\" + state + "\\" + year + "\\" + new_file, otherwise_folder + "\\" + new_file)
					elif os.path.isfile(filtered_folder + "\\" + state + "\\" + year + "\\" + 'crossed' + "\\" + new_file) and os.path.isfile(otherwise_folder + "\\" + new_file) == False:
						shutil.copy(filtered_folder + "\\" + state + "\\" + year + "\\" + 'crossed' + "\\" + new_file, otherwise_folder + "\\" + new_file)
					elif os.path.isfile(filtered_folder + "\\" + state + "\\" + year + "\\" + 'worse_version' + "\\" + new_file) and os.path.isfile(otherwise_folder + "\\" + new_file) == False:
						shutil.copy(filtered_folder + "\\" + state + "\\" + year + "\\" + 'worse_version' + "\\" + new_file, otherwise_folder + "\\" + new_file)
					else:
						print('Sad Panda')


def final_filter(checking_folder_state_yr, renamed_files_state_yr, filtered_folder, deletion_folder):
	'''
	This function is to be used only after all issues associated with files have been checked and organized. This function will move
	files deemed to be duplicates, actual worse version, white space, and no data to "to be deleted" folders, from the renamed files database. It will move files
	that are worse_version pairs, crossed out, to separate folders. Take as input state-year combo
	'''

	# worse_version # crossed out # info not attainable # actual duplicates # no data # whitespace
	folder_contents = os.listdir(checking_folder_state_yr)

	# order matters
	for folder in ['worse_version', 'duplicate', 'crossed', 'info_not_attainable', 'no_data', 'whitespace' ]:
		current_folder = checking_folder_state_yr + "\\" + folder
		if folder == 'worse_version':
			filtered_folder_wor_ver = filtered_folder + "\\" + folder 
			deletion_folder_wor_ver = deletion_folder + "\\" + folder
			for i in [filtered_folder_wor_ver, deletion_folder_wor_ver]:
				if os.path.isdir(i) == False:
					os.makedirs(i)
			if os.path.isdir(current_folder + "\\" + 'Has Additional Info Original Doesnt Have'):
				pairs = os.listdir(current_folder + "\\" + 'Has Additional Info Original Doesnt Have')
				#for matched file pairs
				for pair in pairs:
					if os.path.isfile(renamed_files_state_yr + "\\" + pair):
						
						shutil.move(renamed_files_state_yr + "\\" + pair, filtered_folder_wor_ver + "\\" + pair)
						#print(renamed_files_state_yr + "\\" + pair, filtered_folder_wor_ver + "\\" + pair)
			#actually worse versions
			for element in os.listdir(current_folder):
				if os.path.isfile(renamed_files_state_yr + "\\" + element):
					
					shutil.move(renamed_files_state_yr + "\\" + element, deletion_folder_wor_ver + "\\" + element)
					#print(renamed_files_state_yr + "\\" + element, deletion_folder_wor_ver + "\\" + element)
		if folder == 'crossed':
			filtered_folder_cross = filtered_folder + "\\" + folder
			if os.path.isdir(filtered_folder_cross) == False:
				os.makedirs(filtered_folder_cross)
			for element in os.listdir(current_folder):
				if os.path.isfile(renamed_files_state_yr + "\\" + element):
					
					shutil.move(renamed_files_state_yr + "\\" + element, filtered_folder_cross + "\\" + element)
					#print(renamed_files_state_yr + "\\" + element, filtered_folder_cross + "\\" + element)
		if folder in ['no_data', 'duplicate', 'whitespace', 'info_not_attainable']:
			deletion_folder_other = deletion_folder + "\\" + folder
			if os.path.isdir(deletion_folder_other) == False:
				os.makedirs(deletion_folder_other)
			for element in os.listdir(current_folder):
				if os.path.isfile(renamed_files_state_yr + "\\" + element):
					
					shutil.move(renamed_files_state_yr + "\\" + element, deletion_folder_other + "\\" + element)
					#print(renamed_files_state_yr + "\\" + element, deletion_folder_other + "\\" + element)
	print('Done with %s', current_folder)



def package(input_path, current_path, output_path, stamp):
	'''
	This function is intended to take a general output folder for some file source as input, 
	and output a prepared package into the metadata collection folder. Usually, input_path will be an output folder
	in one of the source folders in manuscript database folder, like output_tiff or output_final. Input_path=current_path when func is called
	Output_path is usally the metadata collection folder
	'''
	if os.path.isdir(current_path) == False:
		rel_path = os.path.relpath(current_path, input_path) 
		#print(rel_path)
		file = rel_path.split("\\")
		#print(file)
		
		#(1) First adjustment
		#just files with one branch, and then all files
		meta = file[0].split("_")

		#meta = file[1].split("_")

		#just for KS 1880 replacing commented out part above with:
		#meta = file[2].split("_")
		#print(file)
		#print(meta, file)
		
		state, year = meta[0], meta[1]
		
		#just for NARA
		#state = 'TX'
		#year = '1880'
		package_folder = output_path + "\\" + state + year + "_" + stamp
		if os.path.isdir(package_folder) == False:
			os.makedirs(package_folder)
		#just for now
		#(2) second adjustment
		#new_path = package_folder + "\\" + file[1]
		
		#for Nara, just files with one branch, and then all files
		new_path = package_folder + "\\" + file[0]
		if os.path.isfile(new_path) == False:
			file_obj = Image.open(current_path)
			width, height = file_obj.width, file_obj.height
			#print(current_path)
			file_obj = file_obj.resize((int(width * shrink_factor), int(height * shrink_factor)), Image.ANTIALIAS)
			#default setting
			#(3) third adjustment
			#file_obj.save(package_folder + "\\" + file[1], optimize = True, quality = quality_factor)
			#for NARA, just files with one branch, and then all files
			file_obj.save(package_folder + "\\" + file[0], optimize = True, quality = quality_factor)
			#for KS1880
			#file_obj.save(package_folder + "\\" + file[2], optimize = True, quality = quality_factor)

	else: 
		folder_contents = os.listdir(current_path)
		#print(current_path)
		for key in folder_contents:
			next_path = current_path + "\\" + key
			package(input_path, next_path, output_path, stamp)
		#dictionario = csv_dict(input_path, input_path, {})
		#csv_write(dictionario, output_path, stamp)





######################################################################
if __name__ == '__main__':
	
	#package(IA_1880_output, IA_1880_output, package_folder, "A")
	#new_path = "D:\\temp_nondropbox\\Adam\\Iowa 1880 (Ancestry) Regen\\Package\\IA8_A"
	#dictionario = csv_dict(new_path, new_path , {})
	#csv_write(dictionario, new_path, "A")
	
	#package(Famsearch_output, Famsearch_output, package_folder, 'F')
	#assigned_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\metadata_collection\\Assigned"
	csv_renaming_folder = "D:\\temp_nondropbox\\Adam\\Csvs for Renaming"
	files_to_rename = "D:\\temp_nondropbox\\Adam\\Renamed Priority Files"
	checking_folder = "D:\\temp_nondropbox\\Adam\\Checking Folder After Renaming"
	to_be_deleted = "D:\\temp_nondropbox\\Adam\\To be Deleted"
	filtered_folder = "D:\\temp_nondropbox\\Adam\\Filtered"
	not_in_crosswalk = "D:\\temp_nondropbox\\Adam\\Renamed Priority Files - by schedule\\Not in crosswalk"
	folder_contents = os.listdir(csv_renaming_folder)

	schedule_crosswalk_csv = "D:\\temp_nondropbox\\Adam\\Renamed Priority Files - by schedule\\file_schedule_crosswalk.csv"
	output_schedule_folder = "D:\\temp_nondropbox\\Adam\\Renamed Priority Files - by schedule"

	rearrange_by_schedule(schedule_crosswalk_csv, csv_renaming_folder, files_to_rename, filtered_folder, not_in_crosswalk ,output_schedule_folder)
	#state_year = "\\" + 'KS' + "\\" + "1870"
	


	'''
	for i in folder_contents:
		file_meta = i.split("_")
		state_abbrev, year = file_meta[0], file_meta[1][:-4]
		state_year = "\\" + state_abbrev + "\\" + year
		if year == '1880':
			final_filter(checking_folder + state_year, files_to_rename + state_year, filtered_folder + state_year, to_be_deleted + state_year)
	'''
	'''

	for i in folder_contents:
		file_meta = i.split("_")
		#i dont want the .csv to be part of year
		state_abbrev, year = file_meta[0], file_meta[1][:-4]
		if year == '1880':
			check_renamed_files( csv_renaming_folder + "\\" + i, files_to_rename + "\\" + state_abbrev + "\\"+ year, checking_folder, 'option2')

	'''
	'''
	folder_list = os.listdir(package_folder)
	#folder_list = os.listdir(assigned_path)

	for i in range(len(folder_list)):
		if folder_list[i].endswith('N'):
			input_path = package_folder + "\\" + folder_list[i]
			#print(input_path)
			if 'KS1860' in input_path:
				continue
			dictionario = csv_dict(input_path, input_path, {})
			csv_write(dictionario, input_path, 'N')
	
	'''
		

