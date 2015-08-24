#!/usr/bin/env python3
"""
A simple tool to create a log of all files and folders on a removable media device such as a CD, BLU-Ray or thumb-drive. This indexer can append a user supplied arbitary name to all files/folders which specifies which removable media entity it can be found on.

Discdex aims to collect metadata on all, or choice, data stored on removable storage devices. The metadata can then be put to use for organising and easily be searched through. Ultimately data can be kept track of more easily with discdex.

The default files scanned for are: avi mpeg mov mp4 wmv
This can easily be changed in the config part of discdex.py

An entry in the indexing file takes the form:

Path to device - Device name - Path to file - File name - File type - Modified - Size

Please report any issues to weleoka@github.com
"""

import os, sys
from time import sleep
from dd_utils import dd_proc, dd_fs, dd_prompt
from dd_utils import mnt_autodetect



### Config and options
FILETYPES = "avi mpeg mpg mov mp4 wmv"  ## File endings to search for
#FILETYPES = "*"    ## Use wildcard * to index all file endings.
OUTPUTFILE = "discdex.txt"  ## Default indexing file.
list_file = "" ## Default human readable list file.


### Main
if __name__ == '__main__': # simultaneously coded as importable module and executable script
    option = "refresh_menu" # Make the initial refreshing of the main menu.
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:

        if not option == "refresh_menu":
            option = input('Enter option: ')

        option = option if option in ['1', '2', '3', '4', '9'] else "refresh_menu"

        if not os.path.isfile(OUTPUTFILE) and option in ['2', '3', '4']:
            print("\nCant find the indexing file %s specified.\n"
                % (OUTPUTFILE))
            print("[1] Input name of custom indexing file.")
            print("[2] Return to main menu.")

            while True:
                option_02 = input('Enter option: ')

                if option_02 == "1":
                    OUTPUTFILE = input('Enter filename: ')

                elif option_02 == "2":
                    option = "refresh_menu"

                    break

                else:
                    print("\nDid not recognise the option: %s. Try again.")


    # Refresh the main menu.
        if option == "refresh_menu":
            print("\n\t - DISCDEX -")
            print("[1] Add entries to index.")
            print("[2] Compile human readable list of entries already in an index.")
            print("[3] Export index as CSV file.")
            print("[4] Print index to terminal.")
            print("[9] Quit.")
            option = None


    # Add entries to indexing file.
        elif option == "1":
            option = "refresh_menu" # Reset the option.

            if dd_fs.check_file_status(OUTPUTFILE): #, "Path-to-device\tDevice-name\tPath-to-file\tFile-name\tFile-type\tModified\tSize"):
                device_name = dd_prompt.device_name(OUTPUTFILE)
                path_to_device = dd_prompt.device_path()

                if dd_fs.check_path_status(path_to_device):
                    print ("\nIndexing... please wait.")
                    ticker = 0  # Keep count of the total files found matching the filetype criteria.

                    for filetype in FILETYPES.split(" "):
                        results = dd_fs.walk_device(path_to_device, filetype)
                        entries = dd_proc.create_indexing_entry(results, filetype, path_to_device, device_name)
                        ticker += len(entries)

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

            sorting_option, list_file, description = dd_prompt.sorting_option(list_file)

            if (sorting_option and list_file and description) is not None:
                dd_fs.check_file_status(list_file, "\tMade using www.github.com/weleoka/discdex\n" + description + "\n")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\nCompiling a human-readable, list of all entries in the index: %s \nWriting to file: %s"
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
                    print("The index seems to be empty.")
                    # delete the new list file.

            else:
                print("\nReturned to main menu.\n")


    # Export an indexing file to the CSV format.
        elif option == "3":
            option = "refresh_menu" # Reset the option.
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Export indexed data to CSV file.")
            csv_file = input('\nGive the new CSV file a name (example.csv): ')
            dd_fs.check_file_status(csv_file)
            ticker = 0

            for line in open(OUTPUTFILE):    # open under default flag -r

                if not line in ['\n', '\r\n']: # Ignore blank lines
                    clean_line = line.replace(',', '_')   # Sanitise commas in dir and filenames.
                    csv_line = clean_line.replace('\t', ',')  # Replace tabs with commas.
                    dd_fs.append_to_file(csv_line, csv_file)
                    ticker += 1

            print("\nCSV %s file created containing %s lines"
                % (csv_file, ticker))
            sleep(2)


    # Print indexing file to current terminal window.
        elif option == "4":  
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nPrinting the index to screen.\n")

            for line in open(OUTPUTFILE):    # open under default flag -r
                print(line)


    # Quit Discdex.
        elif option == "9":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nShutting down... Thanks for using Discdex.\n")

            break

    sys.exit()  # Final death sentence.



# Notes:
# print(datetime.fromtimestamp(os.path.getmtime(result)).strftime("%d%b%Y %H:%M:%S"))
