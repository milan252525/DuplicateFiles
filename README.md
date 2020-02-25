# PRG I - Duplicate files

## User guide

### Introduction

The program is a command-line utility for scanning directory and detecting duplicate files. The output is printed directly into the command-line or a file.

The user can choose which of the following file properties are going to be compared.

-   size
    
-   name
    
-   date
    
-   content
    

### Usage

The program is run in a command-line with the following command:

`python dupefiles.py path arguments`

`path` - path to the scanned directory

### Arguments

| ARGUMENT | DESCRIPTION |
| --- | --- |
| -s (--size) | Compare files by size |
| -n (--name) | Compare files by name |
| -d (--date) | Compare files by date\* |
| -c (--content) | Compare files by content |
| -f (--file) | Output into file |

\*Windows - a creation date, Linux - a date of the most recent edit

The order of arguments doesn't matter.

You can display help message by typing `python dupefiles.py --help`.

**Argument -f**

This argument can be left alone or followed by a path where the output file should be saved.

If it's not followed by a path the output will be saved into a directory from which the command is executed.

Default file name: `duplicate_files_DATE.txt`

### Examples of usage

`python dupefiles.py TestFiles/ -n -c`

Looks for all files with an identical name and content

`python dupefiles.py TestFiles/ --date --size`

Looks for all files with an identical date and size

`python dupefiles.py TestFiles/ -c -d -f`

Looks for all files with an identical date and content, the output will be saved into a directory from which the command is executed as duplicate_files_DATE.txt

`python dupefiles.py TestFiles/ -n -f Documents/`

Looks for all files with an identical name, the output will be saved into a directory called Documents as duplicate_files_DATE.txt

`python dupefiles.py TestFiles/ -n -f Documents/result.txt`

Looks for all files with an identical name, the output will be saved into a directory called Documents as result.txt

### Troubleshooting

**Missing libraries**

All used libraries are distributed with the Python. If they are missing anyway, you can install them with the following command.

`pip install --user hashlib argparse`
