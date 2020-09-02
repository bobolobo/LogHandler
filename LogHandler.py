import argparse
import glob
import shutil
import os
import win32api
import win32file
from pick import pick
from sys import exit  # So Exit works after pyinstaller freezing


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


def clear_destination(destroot):
    """ In the destination drive/folder, remove all existing .log files """

    print("Removing existing destination: ", destroot)

    try:
        shutil.rmtree(destroot, ignore_errors=True)  # Completely remove destination folder
    except OSError as e:
        print("Failed with:", e.strerror)  # look what it says

    return


def drive_finder():
    """ Find all drive types then figure out which ones are removable usb """

    '''drive_types = {
        win32file.DRIVE_UNKNOWN: "Unknown\nDrive type can't be determined.",
        win32file.DRIVE_REMOVABLE: "Removable\nDrive has removable media. This includes all floppy drives and many "
                                   "other varieties of storage devices.",
        win32file.DRIVE_FIXED: "Fixed\nDrive has fixed (nonremovable) media. This includes all hard drives, including "
                               "hard drives that are removable.",
        win32file.DRIVE_REMOTE: "Remote\nNetwork drives. This includes drives shared anywhere on a network.",
        win32file.DRIVE_CDROM: "CDROM\nDrive is a CD-ROM. No distinction is made between read-only and read/write"
                               " CD-ROM drives.",
        win32file.DRIVE_RAMDISK: "RAMDisk\nDrive is a block of random access memory (RAM) on the local computer that "
                                 "behaves like a disk drive.",
        win32file.DRIVE_NO_ROOT_DIR: "The root directory does not exist."
    }'''

    drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]

    removable_count = 0
    removable_volumes = {}

    for device in drives:
        what_type = win32file.GetDriveType(device)
        # print("What type is: ", what_type)

        if what_type == 2:
            removable_count += 1
            device_name = (win32api.GetVolumeInformation(device))
            device_name = str(device_name[0])
            removable_volumes.update({device: device_name})
            values = list(removable_volumes.keys())

    print("\n\n\nAvailable USB drives are: ", removable_volumes)

    values.append('Exit with no pick')  # Add exit option if user changes mind.
    title = 'Please choose Drive to write logs to ' + str(removable_volumes) + ': '
    value, index = pick(values, title, indicator='=>')

    if value != 'Exit with no pick':
        destroot = value + r'Temp\LOGCAPTURE'
        return destroot
    else:
        print("\nExiting with no action based on user selection.")
        exit(1)

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


'''def string_cleaner(temp_dict):
    """ Routine to strip brackets, parens, extra commas, etc from string buffer before writing to csv file """

    # Strip brackets, single quotes, parens from buffer. Matplotlib seems to send data with commas at the end.
    # tempstring = (str(temp_string_buffer).translate(str.maketrans({'[': '', ']': '', '\'': '', ')': '', '(': ''})))

    tempstring = str(temp_dict)
    tempstring = re.sub(r'\\', ',', tempstring)  # Remove double backslashes
    tempstring = re.sub(r',:', '', tempstring)  # Remove Trailing colon
    temp_dict = list(tempstring)
    print("Temp_dict: ", temp_dict)

    # return tempstring
    return
'''

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


def download(destroot):
    """ Download log files to D: USB stick """

    clear_destination(destroot)  # Remove existing .log files in the destination

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
    print("\n" + str(len(file_list)) + " files downloaded to (" + destroot + ") but still remain on the server.")
    print("To delete the log files on the server, run: " + __file__ + " clean")

    return


def main():

    choice = command_line_arguments()

    if choice.action == "clean":
        # drive_finder()
        cleaner()
    elif choice.action == "download":
        destination = drive_finder()
        download(destination)


if __name__ == '__main__':
    main()
