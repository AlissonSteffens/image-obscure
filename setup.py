import pyAesCrypt
import io
from PIL import Image
import sys
from colorama import init
import os
from colorama import Fore, Back, Style
from termcolor import colored
import getpass


file_type = 'picture'
input_types = ['jpg']

def encrypt(file, password):
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile(file, file[:-3]+file_type, password, bufferSize)

def decrypt(file, password):
    bufferSize = 64 * 1024

    with open(file, "rb") as f:
        img_bytes = f.read()
        
    fCiph = io.BytesIO(img_bytes)
    fDec = io.BytesIO()
    ctlen = len(fCiph.getvalue())
    try:
        pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen)
        im = Image.open(fDec)
        return im
    except:
        print(colored('Wrong Password for '+file, 'red',attrs=['bold']))

def list_encryptable_imgs ():
    todos = os.listdir()
    decryptable = []
    for t in todos:
        for i in input_types:
            if ('.'+i) in t:
                decryptable.append(t)
    return decryptable

def list_decryptable_imgs ():
    todos = os.listdir()
    decryptable = []
    for t in todos:
        if ('.'+file_type) in t:
            decryptable.append(t)
    return decryptable

def encript_dialog():
    print('-------------------------')
    print(colored('Encrypt\n', 'white','on_magenta',attrs=['bold']))
    imgs = list_encryptable_imgs()
    count = 1
    for i in imgs:
        print(colored(str(count)+'. ', 'magenta')+i)
        count+=1
    print(colored(str(count)+'. ', 'magenta')+'bulk')
    print('Choose the option:')
    selected = int(input())
    if selected < count:
        selected_img = imgs[selected-1]
        print('Encrypting '+colored(selected_img, 'magenta')+", please enter the password.")
        password = getpass.getpass('Password:')
        image = encrypt(selected_img,password)
    else:
        print('Encrypting all images, please enter the password. (All images will have the same password)')
        password = getpass.getpass('Password:')
        for i in imgs:
            encrypt(i,password)
            print(colored(i, 'magenta')+" encripted.")

def decrypt_dialog():
    print('-------------------------')
    print(colored('Decrypt\n', 'white','on_cyan',attrs=['bold']))
    imgs = list_decryptable_imgs()
    count = 1
    for i in imgs:
        print(colored(str(count)+'. ', 'cyan')+i)
        count+=1
    print(colored(str(count)+'. ', 'cyan')+'bulk')
    print('Choose the option:')
    selected = int(input())
    if selected < count:
        selected_img = imgs[selected-1]
        print('Decrypting '+colored(selected_img, 'cyan')+", please enter the password.")
        password = getpass.getpass('Password:')
        image = decrypt(selected_img,password)
        image.show()
    else:
        print('Decrypting all images.') 
        print('Dou you want to:\n'+colored('1. ', 'cyan',attrs=['bold'])+'Open Images\n'+colored('2. ', 'cyan',attrs=['bold'])+'Save Images\n')
        save = int(input())
        print('please enter the password. (All images must have the same password)')

        password = getpass.getpass('Password:')
        images = []
        for i in imgs:
            images.append(decrypt(i,password))
        
        if save == 1:
            for i in images:
                i.show()
        elif save == 2:
            if not os.path.exists('decrypted'):
                os.makedirs('decrypted')
            count = 0
            for i in images:
                img_name = imgs[count][:-len(file_type)]+'jpg'
                i.save("decrypted/"+img_name)
                print(colored(img_name, 'cyan',attrs=['bold'])+' saved')
                count+=1
        
            

if __name__ == "__main__":
    init()
    print('Do you want to:\n'+colored('1. Encrypt\n', 'magenta',attrs=['bold'])+colored('2. Decrypt\n', 'cyan',attrs=['bold']))
    action = int(input())
    if action == 1:
        encript_dialog()
    elif action == 2:
        decrypt_dialog()
    else:
        print('Unable to find option')