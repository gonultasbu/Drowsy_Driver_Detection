import os
from video_processor import process_video

def subdir_traverser(input_dir):
    file_count=0;
    for root, dirs, files in os.walk(input_dir, topdown=False):
        for name in files:
            if (name.endswith("(1).avi")):
                print(os.path.join(root, name))
                process_video(os.path.join(root,name))
                file_count=file_count+1;
    print (file_count , "VIDEOS ARE PROCESSED")

   #unnecessary part
   #for name in dirs:
   #print(os.path.join(root, name))


#GIVE THE DIRECTORY YOU WANT TO PROCESS AS INPUT
subdir_traverser("C:\\Users\\Mert\\Dropbox\\ITU\\2017 BITIRME\\DATASETS")