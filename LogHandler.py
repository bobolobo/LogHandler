import argparse
import os
from os import listdir
import re
import glob
import shutil


destroot = r'D:\temp\LOGCAPTURE'


def command_line_arguments():
    """Read and evaluate commandline arguments, returns the single commandline argument"""

    try:
        parser = argparse.ArgumentParser(description='Log Handler/Cleaner/Copier for Idemia DocAuth')

        # Add required arguments.
        parser.add_argument('action', choices=['clean', 'download'], type=str, help='clean or download')

        # Parse the arguments
        args = parser.parse_args()

        return args

    except Exception as err:
        print(err)
        return

def clear_destination():
    """ In the destination drive/folder, remove all existing .log files """

    print("Removing existing destination: ", destroot)

    try:
        shutil.rmtree(destroot)  # Completely remove destination folder
    except OSError as e:
        print( "Failed with:", e.strerror )  # look what it says

    return

def find_logs():
    # Get recursive lists of file paths that matches pattern including sub directories

    file_list1 = glob.glob(r'/Program Files/IDEMIA/MFace Flex IAP/log/*.log*', recursive=False)
    file_list2 = glob.glob(r'/Program Files/IDEMIA/MFace Flex IS/log/*.log*', recursive=False)
    file_list3 = glob.glob(r'/Program Files/IDEMIA/MFace Flex WS/logs/*.log*', recursive=False)
    file_list4 = glob.glob(r'/STIP/*.log*', recursive=False)
    file_list5 = glob.glob(r'/ECAT/BioFDRS/*.xml*', recursive=False)

    file_list6 = glob.glob(r'/Program Files/IDEMIA/Cameras/First/*.log*')
    file_list7 = glob.glob(r'/Program Files/IDEMIA/Cameras/Second/*.log*')

    file_list = file_list1 + file_list2 + file_list3 + file_list4 + file_list5 + file_list6 + file_list7

    return file_list

def cleaner():
    """ Remove log files """

    file_list = find_logs()

    # Iterate over the list of filepaths & remove each file.
    for file_path in file_list:
        file_path = os.path.normpath(file_path)  # Reorient path slashes for Windows
        print("File is: ", file_path)
        try:
            os.remove(file_path)
        except OSError as e:
            print("Failed with:", e.strerror)  # look what it says

    return file_list

def download():
    """ Download log files to D: USB stick """

    # destroot = r'D:\temp\LOGCAPTURE'

    clear_destination()  # Remove existing .log \files in the destination

    file_list = find_logs()

    print("\nDownloading files:", )
    for full_file_name in file_list:
        full_file_name = os.path.normpath(full_file_name)
        path_name = os.path.dirname(full_file_name)
        path_name = path_name.lstrip(r'\\')
        destpath = os.path.join(destroot, path_name)
        os.makedirs(destpath, exist_ok=True)
        shutil.copy(full_file_name, destpath)
        print(full_file_name)
    print("\nFiles downloaded to (" + destroot + ") and also remain on server.")
    return


def main():

    choice = command_line_arguments()

    if choice.action == "clean":
        cleaner()
    elif choice.action == "download":
        download()


if __name__ == '__main__':
    main()
