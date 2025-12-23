import hashlib
import os
from base64 import b64encode

#Records and returns the program and associated password

def program_password_input():

    program = input("Program Name: ")
    password = input("Enter Password: ")

    return program, password

#Converts the password to be hash into a utf-8 byte encoding while generating a random salt using the
#os cryptographic library os.urandom

def encode_password(password):

    password_bytes = password.encode("utf-8")
    salt = b64encode(os.urandom(20))

    return password_bytes, salt

#Hashes and salts the password over a fixed number of iterations using sha256

def hash_password(password_bytes, salt):

    iterations = 1000
    password_hash = hashlib.pbkdf2_hmac(
    'sha256',         
    password_bytes,          
    salt,             
    iterations         
    )

    return password_hash

#Checks for a file path and either opens a new file or appends and existing one
#Stores program name, hashed and salted password, and salt value.

def add(program=None, password=None):

    if program is None and password is None:
        program, password = program_password_input()
   
    password_bytes, salt = encode_password(password)
    password_hash = hash_password(password_bytes, salt)

    if os.path.exists("passwords.txt"):
        fh = open("passwords.txt","a")
    else:
        fh = open("passwords.txt",'w')
    
    line = "program: " + program + " " + "hash: " + str(password_hash) + " " + "salt: " + salt.decode("utf-8") + "\n"
    fh.write(line)
    fh.close()

#Parses the text file to retrieve the recorded hashed value.

def retrieve_hash(program):

    hash_value = ""
    fh = open("passwords.txt", "r")

    for line in fh:
        if program in line:
            start_index = line.find("hash: ") + 6
            end_index = line.find("salt: ") - 1
            hash_value = line[start_index:end_index]

    fh.close()
    
    return hash_value

#Parses the text file to retrieve the recorded salt value.

def retrieve_salt(program):

    salt_value = ""
    fh = open("passwords.txt", "r")

    for line in fh:
        if program in line:
            index = line.find("salt: ") + 6
            salt_value = line[index:len(line) - 1]

    fh.close()
    
    return salt_value

#Hashes and salts the inputed password and then compares it to the previously
#stored password to determine if it is a match or not.

def validate():

    program, password = program_password_input()
    password_bytes, _ = encode_password(password)
    salt = retrieve_salt(program).encode("utf-8")
    current_hash = str(hash_password(password_bytes, salt))
    stored_hash = retrieve_hash(program)
    match = current_hash == stored_hash

    if match:
        print("Passwords match!")
    else:
        print("Passwords do not match.")

#Records all data that is not the program and password being deleted.

def extract_data(program):

    fh = open("passwords.txt",'r')
    data = ""

    for line in fh:

        if program not in line:
            data += line

    fh.close()

    return data

#Writes all data minus the program and password being deleted
#into a new file of the same name.

def delete(program=None,password=None):

    if program is None and password is None:
        program, password = program_password_input()
    
    data = extract_data(program)

    fh = open("passwords.txt","w")
    fh.write(data)
    fh.close

#Deletes and then adds the new password.

def update():

    program, password = program_password_input()
    delete(program, password)
    add(program, password)

#Generates and stores a password while returning the password 
#value to the user for future use.

def generate():

    program = input("Program Name: ")
    byte_for_conversion = os.urandom(20)
    password = str(int.from_bytes(byte_for_conversion, byteorder="big"))
    add(program, password)

    print("Generated Password: " + password)


if __name__ == "__main__":

    print("Welcome! To add a password type in add, validate, delete, or generate. Enter q or Q to exit.")
    action = ""

    while True:
        
        action = input("What would you like to do today? ")

        if action == "q" or action == "Q":
            break

        if action == "add" or action == "Add":
            add()
            print("")
        elif action == "validate" or action == "Validate":
            validate()
            print("")
        elif action == "delete" or action == "Delete":
            delete()
            print("")
        elif action == "update" or action == "Update":
            update()
            print("")
        elif action == "generate" or action == "Generate":
            generate()
            print("")