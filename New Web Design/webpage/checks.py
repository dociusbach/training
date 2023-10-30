import re 
import os
from flask import url_for
def concat_four_ints(num1, num2, num3, num4):

    num1 = num1 * 1000
    num2 = num2 * 100
    num3 = num3 * 10

    num3 += num4
    num2 += num3
    num1 += num2
    return num1

def repeated_characters(password):
    letter_repeat = False
    for i in range((len(password)-3)):
        letter_check = ("{0}{1}{2}{3}".format(password[i], password[i] ,password[i] ,password[i]) in password[i:i+4])
        if letter_check:
            letter_repeat = True   
    return letter_repeat

def sequential_numbers(password):
    sequential_check = False
    for i in range((len(password)-3)):
        
        number_check = password[i:i+4]
        
        if number_check.isnumeric():
            number_check = concat_four_ints(int(password[i]), int(password[i+1]) ,int(password[i+2]) ,int(password[i+3]))
            check_pass = concat_four_ints(int(password[i]), int(password[i])+1 ,int(password[i])+2 ,int(password[i])+3)
            if  number_check == check_pass :
                sequential_check = True
                
    return sequential_check  
    


def password_complexity(password):

    min_length = len(password) < 8
    max_length = len(password) > 64
    repeated_char = repeated_characters(password) is True
    sequential_num = sequential_numbers(password) is True
    uppercase_check = re.search(r"[A-Z]", password) is None
    symbol_check = re.search(r"\W", password) is None
    digit_check = re.search(r"\d", password) is None
    lowercase_check = re.search(r"[a-z]", password) is None
    password_pass = not(min_length or max_length or repeated_char or sequential_num or uppercase_check or symbol_check or digit_check or lowercase_check)
    return {
        'password_pass' : password_pass,
        'max_length': max_length,
        'repeated_characters': repeated_char,
        'sequential_numbers' : sequential_num,
        'uppercase_check' : uppercase_check,
        'symbol_check': symbol_check,
        'digit_check': digit_check,
        'lowercase_check': lowercase_check,
    }

def check_image(file_name):
    # set default icon path
    icon_path = url_for('static', filename='images/default-avatar.png')

    #check if path exists
    if file_name is not None:
        path = url_for('static', filename=file_name)
        if os.path.exists(path):
            icon_path = path 
            
    return icon_path

