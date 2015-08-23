#!/usr/bin/env python3

import os, sys
from time import sleep
from dd_utils import dd_proc, dd_fs
from dd_utils import mnt_autodetect
from numbers import Number


"""
Config and options
"""
FILETYPES = "avi mpeg mpg mov mp4 wmv"  ## File endings to search for
#FILETYPES = "*"    ## Use wildcard * to index all file endings.
OUTPUTFILE = "discdex.txt"  ## Default indexing file.
list_file = "" ## Default human readable list file.


"""
Display all device names currently existing in indexing file. 
Prompt for a new device name and then check if user input is unique,
if not unique prompt y/n for continue. 

parameters:
    indexing_file: string. The current indexing file.

return:
    device_name: string. The name of the device to index.
"""
def prompt_device_name(indexing_file):

    current_device = ""
    device_list = []
    for line in dd_fs.read_indexing_file(indexing_file):

        if current_device != line[0]:
            device_list. append(line[0])
            current_device = line[0]

    while True:
        print("\nCurrently indexed device names are:\n%s"
            % (device_list))
        device_name = input('Enter a name for the new device (ex. disc_01): ')

        if device_name in device_list:
            y_n = input("' %s '  as a device name already exists. Do you want to continue anyway? y/n: "
                % (device_name))

            if y_n in ['y', 'n']:

                    if y_n == 'y':
                        break

                    elif y_n == 'n':
                        continue
        break
    return device_name


"""
Display select list of all file systems currently mounted.
Prompt for path to device or one of the select options.

parameters:
   none.

return:
    path_to_device: string. The path to the device to index.
"""
def prompt_device_path():

    mnt_points = mnt_autodetect.get_mount_points()
    i = 0
    print ("\n")
    for mnt_point in mnt_points:
        i = i + 1
        print("[%i] %s %s"
            % (i, mnt_point[0].decode().split('/')[2], mnt_point[1].decode()))

    path_to_device = input('Enter option or path (ex. /media/simoni/superCD ): ') # Use this to have a promt for path to device.
    # path_to_device = "/home/bunnybook/python/discdex" # Use this to have a fixed path location to work from.
    # isinstance(path_to_device, Number) and

    try:
        dev = int(path_to_device)
    except:
        dev = False
        
    if dev and dev <= len(mnt_points):
            path_to_device = mnt_points[dev - 1]
            path_to_device = path_to_device[1].decode()

    return path_to_device


"""
Promt for the sorting method.
[1] Alphabetical order.
[2] Alphabetical order grouped by device name.
Promt for a description to be written to the new list.

parameters:
   list_file: string. The file which will contain the sorted list.

return:
    path_to_device: string. The path to the device to index.
    list_file: string. The file which will contain the sorted list.
"""
def prompt_sorting_option(list_file = ''):
    print("\nChoose a sorting mode for the new list.\n")
    print("[1] Alphabetical order.")
    print("[2] Alphabetical order grouped by device name.")
    print("[9] Main menu.")

    while True:
        sorting_option = input('Enter option: ')

        if sorting_option in ['1', '2']:

            while True:
                list_file = list_file or input('\nGive the new list file a file name: ')    # Use specified or query for new.
                if list_file != '':
                    break

            description = input('\nGive the new list a description (or leave blank): \n')

            return sorting_option, list_file, description

        elif sorting_option == "9":
            return None, None, None


"""
MAIN
"""
if __name__ == '__main__': # simultaneously coded as importable module and executable script
    option = "refresh_menu" # Make the initial refreshing of the main menu.
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        if not option == "refresh_menu":
            option = input('Enter option: ')

        if option in ['1', '2', '3', '9']:
            option = option

        else:
            option = "refresh_menu"

        if not os.path.isfile(OUTPUTFILE) and option in ['2', '3']:
            print("\nCant find the indexing file %s specified.\n"
                % (OUTPUTFILE))
            print("[1] Input name of custom indexing file.")
            print("[2] Return to main menu.")

            while True:
                optionMk2 = input('Enter option: ')

                if optionMk2 == "1":
                    OUTPUTFILE = input('Enter filename: ')

                elif optionMk2 == "2":
                    option = "refresh_menu"
                    break

                else:
                    print("\nDid not recognise the option: %s. Try again.")


    # Refresh the main menu.
        if option == "refresh_menu":

            print("\n\t - DISCDEX -")
            print("[1] Add entries to index file.")
            print("[2] Compile human readable list of entries already in an index file.")
            print("[3] Export indexing file as CSV file.")
            print("[9] Quit.")
            option = None


    # Add entries to indexing file.
        elif option == "1":
            option = "refresh_menu" # Reset the option.

            if dd_fs.check_file_status(OUTPUTFILE): #, "Path-to-device\tDevice-name\tPath-to-file\tFile-name\tFile-type\tModified\tSize"):
                device_name = prompt_device_name(OUTPUTFILE)
                path_to_device = prompt_device_path()

                if dd_fs.check_path_status(path_to_device):
                    print ("\nIndexing... please wait.")

                    ticker = 0  # Keep count of the total files found matching the filetype criteria.

                    for filetype in FILETYPES.split(" "):
                        results = dd_fs.walk_device(path_to_device, filetype)
                        entries = dd_proc.create_indexing_entry(results, filetype, path_to_device, device_name)

                        ticker = ticker + len(entries)

                        for entry in entries:
                            dd_fs.append_to_file(entry, OUTPUTFILE)

                    print("\nDone! Total %i files written to %s... Returning to main menu..."
                        % (ticker, OUTPUTFILE))
                    sleep(3)
                    os.system('cls' if os.name == 'nt' else 'clear')

                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("\nNon-valid path <%s>. Returning to main menu...\n"
                        % (path_to_device))
                    sleep(2)


    # Sort the indexing file and make a human readable list of all entries.
        elif option == "2":
            option = "refresh_menu" # Reset the option.

            sorting_option, list_file, description = prompt_sorting_option(list_file)

            if (sorting_option and list_file and description) is not None:
                dd_fs.check_file_status(list_file, "\tMade using www.github.com/weleoka/discdex\n" + description + "\n")

                os.system('cls' if os.name == 'nt' else 'clear')
                print("\nCompiling a human-readable, list of all entries in the indexing file: %s \nWriting to file: %s"
                    % (OUTPUTFILE, list_file))

                dataset = dd_fs.read_indexing_file(OUTPUTFILE)
                sorted_list = dd_proc.sort_list_of_tuples(dataset, sorting_option)

                if sorted_list is not None:
                    entries, ticker = dd_proc.stringify_list_of_tuples(sorted_list, sorting_option)

                    for entry in entries:
                        dd_fs.append_to_file(entry, list_file)

                    print("\n...Done! Total %i entries written to %s"
                        % (ticker, list_file))
                    sleep(4)

                else:
                    print("The indexing file seems to be empty.")
                    # delete the new list file.

            else:
                print("\nReturned to main menu.\n")


    # Export an indexing file to the CSV format.
        elif option == "3":
            option = "refresh_menu" # Reset the option.

            os.system('cls' if os.name == 'nt' else 'clear')
            print("Export indexing file data to CSV file.")
            csv_file = input('\nGive the new CSV file a name (example.csv): ')
            dd_fs.check_file_status(csv_file)

            f = open(OUTPUTFILE, 'r')
            line = f.readline()
            ticker = 0

            while line:

                if not line in ['\n', '\r\n']: # Ignore blank lines
                    clean_line = line.replace(',', '_')   # Sanitise commas in dir and filenames.
                    csv_line = clean_line.replace('\t', ',')  # Replace tabs with commas.
                    dd_fs.append_to_file(csv_line, csv_file)
                    ticker = ticker + 1

                line = f.readline()

            print("\nCSV %s file created containing %s lines"
                % (csv_file, ticker))
            sleep(2)


    # Quit Discdex.
        elif option == "9":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nShutting down... Thanks for using Discdex.\n")
            break


    sys.exit()  # Final death sentence.


    # Print indexing file to current terminal window.
    '''
        elif option == "4":  
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nPrinting the index file to screen.\n")
            break
    '''

# Notes:
# print(datetime.fromtimestamp(os.path.getmtime(result)).strftime("%d%b%Y %H:%M:%S"))
