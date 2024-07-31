import argparse
from enum import Enum
import os
import stat
import magic
from prettytable import PrettyTable

# I decided to make these permissions unusual for this task, as by default files are not writtable by group or world. I also wanted to make the user to define what permissions they want to detect by themselves, but I did not have enough time to think properly about this solution
class Permission(Enum):
    group_write = stat.S_IWGRP
    world_write = stat.S_IWOTH

def is_unusual_permission(permission_bit):
    return permission_bit & Permission.world_write.value or permission_bit & Permission.group_write.value

def fill_category_table(category_table, categories):
    category_table.field_names = ["Category", "Files", "total_size"]
    for key in categories:
        category_table.add_row([key, categories[key][0], categories[key][1]])

def scandir(directory, categories, threshold, threshold_files, unusual_permission_files, is_recursive):
    for entry in os.scandir(directory):
        file_path = entry.path

        try:
            if entry.is_dir(follow_symlinks=False):
                if is_recursive:
                    scandir(file_path, categories, threshold, threshold_files, unusual_permission_files, is_recursive)
                file_type = 'directory'
            else:
                file_type = magic.from_file(file_path, mime = True)

            if is_unusual_permission(os.stat(file_path).st_mode):
                unusual_permission_files.append(file_path)

            add_file_to_categories(file_path, file_type, categories, threshold, threshold_files)
        
        except(PermissionError):
            print(f"File {file_path} is inaccesible")
        except OSError as error:
            print('Error in os', error)

def add_file_to_categories(file_path, file_type, categories, threshold, threshold_files):
    try:
        size = os.path.getsize(file_path) # For the size of the directory I also use this methos as I do not know what type of size for directory to use 
    except OSError as error:
        print('Error in getsize', error)

    if not file_type in categories:
        categories[file_type] = [[], 0]       
    categories[file_type][0].append(file_path)
    categories[file_type][1] += size

    if not threshold is None and size > threshold:
        threshold_files.append((file_path, size))
       
# print the table with name of the category, list of file paths (including directory) of each category and total size of these files in bytes. If recursive it will investigate all the folders and files in the directory. Otherwise, it won't go into the folders in the directory. 
def analyze_file(directory, threshold, is_recursive):
    categories = {} # key -> category string, value -> [[files of this category], total_size in bytes of files in category]
    large_files = [] # list of files which size in bytes > threshold if treshold is not None
    unusual_permission_files = [] # list of files whith unusual permissions

    scandir(directory, categories, threshold, large_files, unusual_permission_files, is_recursive)
    category_table = PrettyTable()
    fill_category_table(category_table, categories)

    print(category_table)
    print("files with unusual permissions:")
    print(unusual_permission_files)

    if not threshold is None:
        print(f"large files (size > {threshold}):")
        print(large_files)

    return categories, large_files, unusual_permission_files # to demonstrate results in testing

def main(arg_list: list[str] | None = None):
    parser = argparse.ArgumentParser(description='Tool that analyzes and reports on the file system structure and usage on a Linux system')
    parser.add_argument('directory_path')
    parser.add_argument('-r', '--recursive', action="store_true", help='It makes the tool to analyze files in the directory recursevely')
    parser.add_argument('-th', '--threshold', action="store", type=int, help='It makes the tool to print the list of files in the directory that have the size above the threshold (in bytes)')
  
    args = parser.parse_args(arg_list)

    directory_path = args.directory_path
    is_recursevely = args.recursive
    threshold = args.threshold

    if not os.path.exists(directory_path):
        print (f"Directory {directory_path} does not exist")
        return
    
    if not threshold is None and threshold < 0:
        print ("Threshold must not be less than 0")
        return

    analyze_file(directory_path, threshold, is_recursevely)

if __name__ == '__main__':
    main()
