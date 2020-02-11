import argparse
import os
from os import listdir
import re
import glob
import shutil


def command_line_arguments():
    """Read and evaluate commandline arguments, returns the single commandline argument"""

    try:
        parser = argparse.ArgumentParser( description='Log Handler/Cleaner/Copier for Idemia DocAuth' )

        # Add required arguments.
        parser.add_argument( 'action', choices=['clean', 'download'], type=str, help='clean or download' )

        # Parse the arguments
        args = parser.parse_args()

        return args

    except Exception as err:
        print(err)
        return

def clear_destination():
    """ In the destination drive/folder, remove all existing .log files """

    folder_path = r'd:/TEMP/'

    print("Removing existing files in destination: ")

    for file_name in listdir(folder_path):
        if re.search(".log*", file_name):
            real_path = os.path.join(folder_path, file_name)
            os.remove(real_path)
            print(real_path)

    return


def cleaner():
    """ Remove log files """

    # Get recursive lists of file paths that matches pattern including sub directories
    file_list1 = glob.glob(r'/Program Files/IDEMIA/*.log*', recursive=True)
    file_list2 = glob.glob(r'/STIP/*.log*', recursive=False)
    file_list3 = glob.glob(r'/ECAT/BioFDRS/*.log*', recursive=False)
    file_list = file_list1 + file_list2 + file_list3
    #print("FILE LIST: ", file_list)

    # Iterate over the list of filepaths & remove each file.
    for filePath in file_list:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")

    return file_list


def download():
    """ Download log files to D: USB stick """

    dest = r'd:/temp'

    clear_destination()  # Remove existing .log \files in the destination

    file_list1 = glob.glob(r'/Program Files/IDEMIA/*.log*', recursive=True)
    file_list2 = glob.glob(r'/STIP/*.log*', recursive=False)
    file_list3 = glob.glob(r'/ECAT/BioFDRS/*.log*', recursive=False)
    file_list = file_list1 + file_list2 + file_list3

    print("\nDownloading files:", )
    for file_name in file_list:
        shutil.copy(file_name, dest)
        print(file_name)
    return


def main():

    choice = command_line_arguments()

    if choice.action == "clean":
        cleaner()
    elif choice.action == "download":
        download()


if __name__ == '__main__':
    main()
