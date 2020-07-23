import argparse
import os
# from os import listdir
# import re
import glob
import shutil
# import pathlib


destroot = r'D:\Temp\LOGCAPTURE'


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
        shutil.rmtree(destroot, ignore_errors=True)  # Completely remove destination folder
    except OSError as e:
        print("Failed with:", e.strerror)  # look what it says

    return

def find_logs():
    """ Get lists of file paths that matches pattern """

    file_list_targets = [r'/Program Files/IDEMIA/MFace Flex IAP/log/*.log*',
                         r'/Program Files/IDEMIA/MFace Flex IS/log/*.log*',
                         r'/Program Files/IDEMIA/MFace Flex WS/logs/*.log*',
                         r'/STIP/*.log*',
                         r'/ECAT/BioFDRS/*.xml*',
                         r'/Program Files/IDEMIA/Cameras/First/*.log*',
                         r'/Program Files/IDEMIA/Cameras/Second/*.log*']

    file_lists_of_lists = [glob.glob(i, recursive=False) for i in file_list_targets]

    # Flatten out the list of lists into one list
    file_list = []
    for i in file_lists_of_lists:
        file_list.extend(i)

    return file_list

def cleaner():
    """ Remove log files """

    file_list = find_logs()

    print("\nRemoving the following log files from server: \n")
    file_count = 0

    # Iterate over the list of filepaths & remove each file.
    for file_path in file_list:

        file_path = os.path.normpath(file_path)  # Reorient path slashes for Windows
        print("Removing: ", file_path)

        try:
            os.remove(file_path)
            file_count += 1
        except OSError as e:
            print("Failed with:", e.strerror)  # look what it says
            # file_count -= 1

    print("\nRemoved a total of " + str(file_count) + " files from the server.")

    return file_list

def download():
    """ Download log files to D: USB stick """

    clear_destination()  # Remove existing .log files in the destination

    file_list = find_logs()

    print("\nDownloading files to destination:", )
    for full_file_name in file_list:
        full_file_name = os.path.normpath(full_file_name)
        path_name = os.path.dirname(full_file_name)
        path_name = path_name.lstrip(r'\\')
        destpath = os.path.join(destroot, path_name)
        os.makedirs(destpath, exist_ok=True)
        shutil.copy(full_file_name, destpath)
        print(full_file_name)
    print("\n" + str(len(file_list)) + " files downloaded to (" + destroot + ") also remaining on server.")
    print("To delete the log files on the server, run: " + __file__ + " clean")
    return


def main():

    choice = command_line_arguments()

    if choice.action == "clean":
        cleaner()
    elif choice.action == "download":
        download()


if __name__ == '__main__':
    main()
