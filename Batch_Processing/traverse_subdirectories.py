import os

def subdir_traverser(input_dir):
    file_count=0;
    for root, dirs, files in os.walk(input_dir, topdown=False):
        for name in files:
            if (name.endswith("(1).avi")):
                print(os.path.join(root, name))
                #function(os.path.join(root,name)
                file_count=file_count+1;
    print (file_count , "VIDEOS ARE PROCESSED")

   #for name in dirs:
   #  print(os.path.join(root, name))



subdir_traverser("/Users/bmg/Dropbox/ITU/2017 BITIRME/Datasets")