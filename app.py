# from flask import Flask
# from flask_cors import CORS
import os
# from dotenv import load_dotenv

# load_dotenv()

import cv2

harcascade_file_name = os.environ.get("HAARCASCADE_FILE_NAME",False)


def opencv():
    cascade = cv2.data.haarcascades
    if harcascade_file_name:    
        path = os.path.join(cascade, harcascade_file_name)
        if(os.path.exists(path)):
            print("File Exist")
            return
        print(" File Not Exist")
    # print(f" HaarCadcade abs Path : {os.path.abspath(cascade+haarcascadeFIle)}\n HaarCascade Path Rel : {cascade}")

opencv()



