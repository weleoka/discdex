#!/usr/bin/env python3

import os, sys
from time import sleep
from dd_utils import dd_proc, dd_fs
from dd_utils import mnt_autodetect
from numbers import Number


"""
Config and options
"""
FILETYPES = "avi mpeg mpg mov mp4 wmv"
#FILETYPES = "*"
OUTPUTFILE = "discdex.txt"



"""
MAIN
"""
if __name__ == '__main__': # simultaneously coded as importable module and executable script

    option = "refresh_menu" # Make the initial refreshing of the main menu.
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        if not option == "refresh_menu":
            option = input('Enter option: ')

        if option == "1" or option == "2" or option == "3" or option == "9":
            option = option
        else:
            option = "refresh_menu"

        if not os.path.isfile(OUTPUTFILE) and (option == "2" or option == "3"):
            print("\nCant find the indexing file %s specified.\n"
                % (OUTPUTFILE))
            print("[1] Input name of custom indexing file.")
            print("[2] Go back to Discdex main.")

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
        elif option == "1" and dd_fs.check_file_status(OUTPUTFILE): #, "Path-to-device\tDevice-name\tPath-to-file\tFile-name\tFile-type\tModified\tSize"):
            option = "refresh_menu" # Reset the option.

            device_name = input('\nYour name for the device (ex. disc_01): ')

            mnt_points = mnt_autodetect.get_mount_points()
            i = 0
            print ("\n")
            for mnt_point in mnt_points:
                i = i + 1
                print("[%i] %s"
                    % (i, mnt_point[1].decode()))

            path_to_device = input('\nPath to disc (ex. /media/simoni/superCD ): ') # Use this to have a promt for path to device.
            # path_to_device = "/home/bunnybook/python/discdex" # Use this to have a fixed path location to work from.
            # isinstance(path_to_device, Number) and

            try:
                dev = int(path_to_device)
            except:
                dev = False
            if dev and dev <= len(mnt_points):
                    path_to_device = mnt_points[dev - 1]
                    path_to_device = path_to_device[1].decode()

            if dd_fs.check_path_status(path_to_device):
                print ("\nIndexing... please wait.")

                ticker = 0  # Keep count of the total files found matching the filetype criteria.

                for filetype in FILETYPES.split(" "):
                    results = dd_fs.walk_device(path_to_device, filetype)
                    entries = dd_proc.create_indexing_entry(results, filetype, path_to_device, device_name)

                    ticker = ticker + len(entries)

                    for entry in entries:
                        dd_fs.append_to_file(entry, OUTPUTFILE)

                os.system('cls' if os.name == 'nt' else 'clear')
                print("\nDone! Total %i files written to %s... Returning to main menu..."
                    % (ticker, OUTPUTFILE))
                sleep(2)

            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\nNon-valid path <%s>. Returning to main menu...\n"
                    % (path_to_device))
                sleep(2)

    # Sort the indexing file and make a human readable list of all entries.
        elif option == "2":
            option = "refresh_menu" # Reset the option.

            print("\nChoose a sorting mode for the new list.\n")
            print("[1] Alphabetical order.")
            print("[2] Alphabetical order grouped by device name.")
            print("[9] Main menu.")

            while True:
                sorting_option = input('Enter option: ')
                if sorting_option == "1" or sorting_option == "2":
                    list_file = input('\nGive the new list file a file name: ')
                    description = input('\nGive the new list a description (or leave blank): \n')

                    dd_fs.check_file_status(list_file, "\tMade using www.github.com/weleoka/discdex\n" + description + "\n")

                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("\nCompiling a human-readable, list of all entries in the indexing file: %s"
                        % (OUTPUTFILE))
                    print("\nWriting to file: %s"
                        % (list_file))

                    dataset = dd_fs.read_indexing_file(OUTPUTFILE)
                    sorted_list = dd_proc.sort_list_of_tuples(dataset, sorting_option)
                    entries, ticker = dd_proc.stringify_list_of_tuples(sorted_list, sorting_option)

                    for entry in entries:
                        dd_fs.append_to_file(entry, list_file)

                    print("\n...Done! Total %i entries written to %s"
                        % (ticker, list_file))
                    sleep(4)
                    break

                elif sorting_option == "9":
                    break



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


    sys.exit()



# Notes:
# print(datetime.fromtimestamp(os.path.getmtime(result)).strftime("%d%b%Y %H:%M:%S"))
