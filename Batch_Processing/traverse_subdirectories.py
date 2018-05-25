# -*- coding: utf-8 -*-
import os
from video_processor import process_video
from batch_evaluation import eval_func

def subdir_traverser_print(input_dir):
    file_count=0;
    for root, dirs, files in os.walk(input_dir, topdown=False):
        for name in files:
            if (name.endswith("(1).avi")):
                print(os.path.join(root, name))
                file_count=file_count+1;
    print str(file_count) + " VIDEOS EXIST"


def subdir_traverser_video(input_dir):
    file_count=0;
    for root, dirs, files in os.walk(input_dir, topdown=False):
        for name in files:
            if (name.endswith(".avi")):
                print(os.path.join(root, name))
                process_video(os.path.join(root,name))
                file_count=file_count+1;
    print str(file_count) + " VIDEOS ARE PROCESSED"

def subdir_traverser_eval(input_dir):
    file_count=0;
    for root, dirs, files in os.walk(input_dir, topdown=False):
        for name in files:
            if (name.endswith("(1).avi.txt")):
                print(os.path.join(root, name))
                file_count=file_count+1;
                type_list=name.split()
                for root_2, dirs_2, files_2 in os.walk(root, topdown=False):
                    for name_2 in files_2:
                        if (name_2.endswith(type_list[0]+"_drowsiness.txt")):
                            print(os.path.join(root_2, name_2))
                            eval_func(os.path.join(root_2, name_2),os.path.join(root, name))



    print str(file_count) + " TEXT FILES ARE COMPARED"


#GIVE THE DIRECTORY YOU WANT TO PROCESS AS INPUT
subdir_traverser_eval("C:\\Users\\Mert\\Dropbox\ITU\\2017 BITIRME\\DATASETS\\BIG_DATASET\\Training_Evaluation_Dataset\\Training Dataset\\001\\glasses")