"""
Utility module for Discdex.
Functions return information data to stdout and take user input for processing.
"""

from dd_utils import mnt_autodetect


def device_name(indexing_file):
    """
    Display all device names currently existing in indexing file. 
    Prompt for a new device name and then check if user input is unique,
    if not unique prompt y/n for continue. 

    parameters:
        indexing_file: string. The current indexing file.

    return:
        device_name: string. The name of the device to index.
    """
    current_device = ""; device_list = []

    for line in open(indexing_file):    # open under default flag -r

        if current_device != line[0]:
            device_list.append(line[0])
            current_device = line[0]

    while True:
        print("\nCurrently indexed device names are:\n%s"
            % (device_list))
        device_name = input('Enter a name for the new device (ex. disc_01): ')

        if device_name in device_list:
            y_n = input("' %s '  as a device name already exists. Do you want to continue anyway? y/n: "
                % (device_name))

            if y_n in ['y', 'n']:

                    if y_n == 'y': break

                    elif y_n == 'n': continue

        elif device_name != "":
            return device_name


def device_path():
    """
    Display select list of all file systems currently mounted.
    Prompt for path to device or one of the select options.

    parameters:
       none.

    return:
        path_to_device: string. The path to the device to index.
    """
    mnt_points = mnt_autodetect.get_mount_points()
    i = 0
    print ("\n")

    for mnt_point in mnt_points:
        i += 1
        print("[%i] %s %s"
            % (i, mnt_point[0].decode().split('/')[2], mnt_point[1].decode()))

    path_to_device = input('Enter path (ex. /media/simoni/superCD ) or choose from above options: ')

    try:
        dev = int(path_to_device)

    except ValueError as e:
        print ("The argument does not contain numbers\n%s" % (e))
        dev = False
        
    if dev and dev <= len(mnt_points):
            path_to_device = mnt_points[dev - 1]
            path_to_device = path_to_device[1].decode()

    return path_to_device


def sorting_option():
    """
    Promt for the sorting method.
    [1] Alphabetical order.
    [2] Alphabetical order grouped by device name.
    Promt for a description to be written to the new list.

    parameters:
       
    return:
        path_to_device: string. The path to the device to index.
        list_file: string. The file which will contain the sorted list.
    """
    print("\nChoose a sorting mode for the new list.\n")
    print("[1] Alphabetical order.")
    print("[2] Alphabetical order grouped by device name.")
    print("[9] Main menu.")

    while True:
        sorting_option = input('Enter option: ')

        if sorting_option in ['1', '2']:

            while True:
                list_file = input('\nGive the new list file a file name: ')    # Use specified or query for new.
                
                description = input('\nGive the new list a description (or leave blank): \n')

                if list_file != '': break

            return sorting_option, list_file, description

        elif sorting_option == "9": return None, None, None