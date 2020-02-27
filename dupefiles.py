#Duplicitní soubory - zápočtový program
#Milan Abrahám
#NPRG030 Programování I

import os 
import json
from datetime import datetime
from time import time 
import argparse #parsing cli arguments
from sys import exit
import hashlib #hashing file content

LENGTH_TO_READ = 65536 #64KB

#function for hashing file content into SHA3-256
def hash_file(path: str):
    hash = hashlib.sha256()
    try:
        with open(path, "rb") as file:
            fb = file.read(LENGTH_TO_READ)
            while len(fb) > 0:
                hash.update(fb)
                fb = file.read(LENGTH_TO_READ)
    #user may not have permissions to access the file, return empty string
    except (PermissionError, OSError):
        return ""
    #return hex hash as a string
    return hash.hexdigest()

#goes through original_path and maps its content into dict
#size, date, name, content - CLI arguments
def dir_to_dict(original_path: str, size: bool, date: bool, name: bool, content: bool):
    #nested function for recursion into subdirectory
    def scan_dir(path):
        try:
            #iterator with all files and directories in the path
            with os.scandir(path) as scanned_files:
                #loop over every entry
                for entry in scanned_files:
                    if entry.is_file():
                        #retrieve file stats
                        stats = entry.stat()
                        #list of keys in the output dict the entry will be saved in
                        dict_path = []
                        if name:
                            #file name
                            dict_path.append(entry.name)
                        if size:
                            #file size in bytes
                            dict_path.append(f"{stats.st_size}B")
                        if date:
                            #Windows - date of creation, Unix - date of the most recent change
                            #timestamp to to string, int()to omit milliseconds
                            dict_path.append(datetime.fromtimestamp(int(stats.st_ctime)).strftime('%Y_%m_%d %H:%M'))

                        #current part of output dict
                        part = output
                        #loop over keys the entry should be saved in, except the last one
                        for key in dict_path[:-1]:
                            #creates the key if it does not exist, if it does exist does nothing
                            part.setdefault(key, {})
                            #recursivily dive into the dictionary
                            part = part[key]
                        #place file paths into dictionary
                        if dict_path[-1] not in part:
                            part[dict_path[-1]] = [entry.path]
                        else:
                            part[dict_path[-1]].append(entry.path)
                    #if entry is directory recursively scan it, skip links
                    elif entry.is_dir() and not entry.is_symlink():
                        scan_dir(entry.path)
        #user may not have permissions to access the directory
        except PermissionError:
            print(f"ERROR: missing permission for {path}")

    #if user chose only content, scan for same size of file instead
    #only files with identical size will be later compared by hashed content
    if content and not size and not date and not name:
        size = True
    #output dict
    output = {}
    scan_dir(original_path)
    return output

#find duplicate entries in the dictionary outputted by dir_to_dict()
#size, date, name, content - CLI arguments
#output - CLI arg, file to output result into
def find_duplicates(dictionary: dict, size: bool, date: bool, name: bool, content: bool, output):
    #the dictionary does not have a set depth, need to recursively dive into it
    def recursion(dictionary, key_path):
        #loop over every key and value in the dictionary
        for key, value in dictionary.items():
            #if the value isn't list keep using recursion on it
            if not isinstance(value, list):
                recursion(value, (key_path + (' ' if len(key_path) > 0 else '') + str(key)))
            #if the value is list, check for duplicates
            else:
                #skip list with one entry, can't have duplicates
                if len(value)>1:
                    text = ""
                    if not content:
                        #identical properties
                        text += f"[{len(value)}]{key_path}{' ' if len(key_path) > 0 else ''}{str(key)}\n"
                        for item in value:
                            #file paths
                            text += f" - {item}\n"
                    #if looking for identical content, compare hashes of files with the rest of properties identical
                    else:
                        hashes = {}
                        for item in value:
                            #hash file
                            hash = hash_file(item)
                            #file error
                            if hash == "":
                                continue
                            #place hashes into dictionary
                            if hash not in hashes:
                                hashes[hash] = [item]
                            else:
                                hashes[hash].append(item)
                        #look for duplicate hashes
                        for file_hash, file_paths in hashes.items():
                            if len(file_paths) > 1:
                                #identical properties
                                text += f"[{len(file_paths)}]{key_path}{' ' if len(key_path) > 0 else ''}{str(key)}\n"
                                for p in file_paths:
                                    #file paths
                                    text += f" - {p}\n"
                    if output is not None:
                        output_file.write(text)
                    else:
                        print(text, end="")
    #prepare file if user wants output into file 
    if output is not None:
        #name containing current date to prevent overwriting previous outputs
        name = f"duplicate_files_{datetime.fromtimestamp(int(time())).strftime('%Y_%m_%d_%H:%M:%S')}.txt"
        #fix the file name if its missing .txt or if it ends with /
        if output[-4:] != ".txt" and output != "":
            if output[-1] != "/" or output[-1] != "\\":
                output += "/"
            output += name
        try:
            #open the file in write mode
            output_file = open(output if output != "" else name, "w")
            #run the recursive function
            recursion(dictionary, "")
            #print message after successfully finishing
            print(f"\nRESULT:\n-> {os.path.realpath(output_file.name)}")
            output_file.close()
        #if the file name is invalid print error and exit
        except FileNotFoundError:
            print("ERROR: Invalid output file name!")
            exit()
    #output will be printed into console
    else:
        print("\nRESULT:\n")
        recursion(dictionary, "")
        print()

if __name__ == "__main__":
    #command line arguments
    #create ArgumentParser object with help message (-h argument)
    parser = argparse.ArgumentParser(description="Scan a specified directory for duplicate files. Use arguments to determine what file properties should be considered.")
    #non-optional argument containing directory to scan
    parser.add_argument("directory_path", type=str, help="directory to scan for duplicate files (recursively)")
    #optional arguments
    parser.add_argument("-s", "--size", action="store_true", help="size")
    parser.add_argument("-d", "--date", action="store_true", help="date of creation (Unix - date of the most recent change)")
    parser.add_argument("-n", "--name", action="store_true", help="name")
    parser.add_argument("-c", "--content", action="store_true", help="content")
    #debug argument, prints more info, saves dictionary outputted by dir_to_dict() into JSON file
    parser.add_argument("--debug", action="store_true", help="debug")
    parser.add_argument("-f", "--file", type=str, action="store", help="store result into a text file", nargs='?', const="")
    #parse arguments into argparse.Namespace (object with CLI arguments)
    args = parser.parse_args()
    #check for missing arguments
    if not args.size and not args.date and not args.name and not args.content:
        print("ERROR: Please use arguments to set what file properties to scan. Use dupefiles.py -h for more info.")
        exit()
    #start time
    start = time()
    #print selected arguments
    print("Looking for files with following duplicate properties:", '\n-name' if args.name else '', '\n-size' if args.size else '', '\n-date' if args.date else '', '\n-content' if args.content else '')
    #run dir_to_dict on the directory_path argument
    scanned = dir_to_dict(args.directory_path, args.size, args.date, args.name, args.content)
    if args.debug:
        print(f"Scanning completed in: {'%.5f'%(time() - start)}s") #5 decimals
        with open('result.json', 'w') as fp:
            json.dump(scanned, fp, indent=4)
    #run find_duplicates on dictionary outputted by dir_to_dict
    find_duplicates(scanned, args.size, args.date, args.name, args.content, args.file)
    #print how long the program took
    print(f"Completed in: {'%.5f'%(time() - start)}s") #5 decimals