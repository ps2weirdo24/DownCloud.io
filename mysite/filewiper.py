import os
from datetime import datetime

log_file = open("wiper_log.txt", "a")
current_files = os.listdir("mysite/downloads/")
file_record_handle = open("file_record.txt", "r")
file_record = file_record_handle.readlines()
file_record_handle.close()
timestamp = (datetime.now()).strftime("%m/%d/%Y - %H:%M")

log_file.write("\n" + timestamp)

for item in current_files:
	if (item + "\n") in file_record:
		os.remove(("mysite/downloads/" + str(item)))
		file_record.remove((item + "\n"))
		log_file.write("\nDeleted: " + item)
	elif (item + "\n") not in file_record:
		file_record.append(item)
	else:
		log_file.write("Error with filewiper process")

write_record = open("file_record.txt","w")

for item in file_record:
	this_entry = (str(item) + "\n")
	write_record.write(this_entry)

write_record.close()
log_file.write("\n======END======")
log_file.close()
