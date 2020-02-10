import argparse
import os
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


def cleaner():
    """ Remove log files """

    # Get recursive lists of file paths that matches pattern including sub directories
    file_list1 = glob.glob('/Program Files/IDEMIA/*.log*', recursive=True)
    file_list2 = glob.glob('/STIP/*.log*', recursive=False)
    file_list = file_list1 + file_list2
    print(file_list)

    # Iterate over the list of filepaths & remove each file.
    for filePath in file_list:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")

    return file_list


def download():
    """ Download log files to D: USB stick """

    dest = r'd:\temp'

    file_list1 = glob.glob('/Program Files/IDEMIA/*.log*', recursive=True)
    file_list2 = glob.glob('/STIP/*.log*', recursive=False)

    file_list = file_list1 + file_list2

    print("Downloading files:", )
    for file_name in file_list:
        shutil.copy(file_name, dest)
        print(file_name)
    return


def main():

    choice = command_line_arguments()
    print(choice.action)

    if choice.action == "clean":
        cleaner()
    elif choice.action == "download":
        download()


if __name__ == '__main__':
    main()
