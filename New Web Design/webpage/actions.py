import uuid 
from flask import request, redirect, flash
from flask import current_app as app
import hashlib
import re
import os
from PIL import Image
from collections import defaultdict

def set_uuid_file(fileName):
    
    
    hex_string = hashlib.md5(fileName.encode("UTF-8")).hexdigest()
    return uuid.UUID(hex=hex_string)

def check_extension(fileName):
    extension = fileName[-4:]
    
    extension_check = re.search('[.]', extension) is None
    
    if extension_check is True:
        extension = fileName[-5:]
        extension_check = re.search('[.]', extension) is None
        
    return {
        'extension_check' : extension_check ,
        'extension' :   extension
    }
            


def check_file(fileName):
    check_ext = check_extension(fileName)
    extension = check_ext['extension']
    extension_check = check_ext['extension_check']
    
    if extension_check is True:
        return {
            "pass" : False,
            "response" : "Image is not a support file type"
        }
    else:
    
        filename = '{0}{1}'.format(set_uuid_file(fileName), extension)
        return{
            "pass" : True,
            "reponse" : "Checks Passed",
            "newfilename" : filename
        }
def upload_image():

    save_path = 'static/images/'
    send_path = 'images/'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(category='error', message='No file part')
            return {
                "upload": "Failed"
            }
        file = request.files['file']
        checkFile = check_file(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash(category='error', message= 'No selected file')
            return {
                "upload": "Failed"
            }
        if checkFile['pass'] is False:
            flash(category='error', message=checkFile['response'])
            return {
                "upload": "Failed"
            }
        if file and checkFile['pass']:
            filename = checkFile['newfilename']
            new_path = os.path.join(app.root_path, save_path, filename)
            sent_path = os.path.join( send_path, filename)
            file.save(new_path)
            image = Image.open(new_path)
            new_image = image.resize((30, 30))
            new_image.save(new_path)
            return {
                "upload": "Pass",
                "newPath" : sent_path
            }
        
# restricts access to senstive user information
# use case in dbfunctions/display_group_members()
def serialize_user_information(user):
    
    return {
        
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'iconFile': user.iconFile,
        
    }
