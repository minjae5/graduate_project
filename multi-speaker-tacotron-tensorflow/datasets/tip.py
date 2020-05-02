import os
specific_folder = 'son/assets/'
file_list = os.listdir(specific_folder)
cnt = 0
for file in file_list:
	if len(file) == 14:
		cnt = cnt+1
		abp = specific_folder+file
		f = open(abp)
		linenum = f.readlines()
if len(linenum) == 1:
	print(file)
	print(cnt)
