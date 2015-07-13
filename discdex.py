#!/usr/bin/env python3

import re, os, fnmatch, sys



"""
Config and options
"""
FILETYPES = "avi mpeg mpg mov mp4 wmv"
#FILETYPES = "*"
OUTPUTFILE = "discdex.txt"


"""
Check status of a file, does it exist or not?
If the file does not exist - create it. Optionally, in the code, with an inital legend.

parameters:
    destination: string. the indexing file to check status of.
    initial_line: string. The first line of the new file. A legend, or some other text.

return:
    boolean
"""
def check_file_status(destination, initial_line = ""):

    if os.path.isfile(destination):
        print("\n[1] Append.")
        print("[2] Over-write.")
        option = input("The file being written to exists. What do you want to do? ")
        if option == "1":
            return True
        elif option == "2":
            myfile = open(destination, 'w')
            myfile.write(initial_line)
            myfile.close()
        else:
            print("Not a recognised option. Exiting")
            sys.exit()

    else:
        print("The file - %s - could not be found... creating it."
            % (destination))
        myfile = open(destination, 'w')
        myfile.write(initial_line)
        myfile.close()
        return True



"""
Check status of path to storage device.

parameters:
    path: string. The directory path to check for validity.

return:
    boolean
"""
def check_path_status(path):
    if os.path.exists(path):
        print("Path valid.")
        return True
    else:
        print("The path %s appears to not exist. Sorry."
            % (path))
        return False



"""
Append to data to file.
The open() function is used with the "a" for append argument.
If the destination file does not exist python creates it.

parameters:
    entry: string. An entry with file metadata to append to the indexing file
    destination: string. the indexing file to append the information to.

return:
    void
"""
def append_to_file(entry, destination):

    myfile = open(destination, 'a')

    myfile.write(entry)
    myfile.close()



"""
Walk the device's directory tree and add files matching the criteria to list.

parameters:
    path_to_device: string. Root path to work from.
    filetype: string. The file types to list.

return:
    results: list. The list of all files of specific filetype found.
"""
def walk_device(path_to_device, filetype):

    results = []

    for root, dirnames, filenames in os.walk(path_to_device):
        for filename in fnmatch.filter(filenames, '*.' + filetype):
            results.append(os.path.join(root, filename))    # /home/bunnybook/python/discdex/FOLDERPHAT/ccc.mp4

    print("Found %s files with ending: %s"
        % (len(results), filetype))

    return results



"""
Create indexing entry/string of file metadata and append to list.
Data should include:
    - Path to device (supplied by user at prompt)
    - Location device name (supplied by user at prompt)
    - Path to file
    - Name of file
    - File type
    - Date modified
    - Size

parameters:
    results: list. All the files found with relevan metadata.
    current_file_type: string. The current filetype being listed.
    path_to_device: string. The path to the currently indexed storage device.
    device_name: string. The user supplied name for the device.

return:
    entries: list. All the files with their stats as string.
"""
def create_indexing_entry(results, current_file_type, path_to_device, device_name):
    entries = []

    for result in results:
        file_full_name = os.path.basename(result)

        if current_file_type == '*':
            file_type = (re.split('\.', file_full_name))[-1]  # This is so that a file type can be assigned to the current entry.
        else:
            file_type = current_file_type

        name = re.split('.' + file_type, file_full_name)[0]

        path_and_name_to_file = re.split(path_to_device, result)[1]

        try:
            path_to_file = re.split(name, path_and_name_to_file)[0]
        except:
            path_to_file = 'ERROR: bad character range'
            print("\n Problem with name of file: %s "
                % (path_and_name_to_file))
            pass

        entries.append('\n'
            + path_to_device + '\t'                     # System path to device
            + device_name  + '\t'                       # Device name
            + path_to_file + '\t'                           # Path to file
            + name + '\t'                                   # Name of file
            + file_type + '\t'                                  # File type
            + str(os.path.getmtime(result)) + '\t'  # Date modified
            + str(os.path.getsize(result))              # Size
            )
    return entries



"""
Take the file name and device name from index file entries and sort them according to sorting_option.
[1] Alphabetical order.
[2] Alphabetical order grouped by device name.
http://www.pythoncentral.io/how-to-sort-python-dictionaries-by-key-or-value/
http://www.thegeekstuff.com/2014/06/python-sorted/

parameters:
    sorting_option: integer. The method of sorting.
    data: list. A list to be sorted.

return:
    sorted_list: list. A list of the sorted entries.
"""
def sort_list_of_tuples(sorting_option, data):

    def getKey(item):
        return item[1].lower()  # Sort by File name and disregard upper-lower case.

    if sorting_option == "1":
        return sorted(data, key=getKey)
        # return sorted(data, key=lambda tup: tup[1])
    elif sorting_option == "2":
        print("\nTHIS MODE NOT SUPPORTED. SORTING ALPHABETICALLY ONLY IN THIS VERSION OF DISCDEX. ")
        return sorted(data, key=getKey())
    else:
        print("error in sorting mode.")
        sys.exit()




"""
Read the indexing file line by line and get file and device name data pairs.
Open indexing file with r-tag for read only access.

parameters:
    source: string. the indexing file to read information from.

return:
    entries: list. A list of the sorted entries.
"""
def read_indexing_file(source):

    t = []
    f = open(source, 'r')
    line = f.readline()

    while line:
        if not line in ['\n', '\r\n']: # Ignore blank lines

            arr = re.split('\t', line)

            # 1, 3 and 4 represent the list index locations of device, and file name  and type respectively.
            try:
                t.append((arr[1], arr[3] + "." + arr[4]))
            except:
                print("Came across faulty entry: %s"
                    % (arr))
                pass

        line = f.readline()

    f.close()

    return t


# p.92 in Think Python for string comparison.
"""
Because tuples are immutable, they don’t provide methods like sort and reverse, which
modify existing lists. But Python provides the built-in functions sorted and reversed,
which take any sequence as a parameter and return a new list with the same elements
in a different order.
"""


"""
MAIN
"""
if __name__ == '__main__': # simultaneously coded as importable module and executable script
    print("\n\t - DISCDEX -")
    print("[1] Add entries to index file.")
    print("[2] Compile human readable list of entries already in index file.")
    option = input('Enter option: ')

# Add entries to indexing file.
    if option == "1":

        check_file_status(OUTPUTFILE) #, "Path-to-device\tDevice-name\tPath-to-file\tFile-name\tFile-type\tModified\tSize")

        device_name = input('\nYour name for the device (ex. disc_01): ')

        path_to_device = input('\nPath to disc (ex. /media/simoni/superCD ): ') # Use this to have a promt for path to device.
        # path_to_device = "/home/bunnybook/python/discdex" # Use this to have a fixed path location to work from.

        if check_path_status(path_to_device):
            print ("\nIndexing... please wait.")

            ticker = 0  # Keep count of the total files found matching the filetype criteria.

            for filetype in FILETYPES.split(" "):
                results = walk_device(path_to_device, filetype)
                entries = create_indexing_entry(results, filetype, path_to_device, device_name)

                ticker = ticker + len(entries)

                for entry in entries:
                    append_to_file(entry, OUTPUTFILE)

            print("\nDone! Total %i files written to %s"
                % (ticker, OUTPUTFILE))
        else:
            sys.exit()

# Sort the indexing file and make a human readable list of all entries.
    elif option == "2":
        print("\n[1] Alphabetical order.")
        print("[2] Alphabetical order grouped by device name.")
        sorting_option = input('Enter list sorting option: ')
        list_file = input('\nGive the list file a file name: ')
        description = input('\nGive the list a description: ')

        check_file_status(list_file, "Made using www.github.com/weleoka/discdex\n" + description + "\n")

        print("\nCompiling a human-readable, list of all entries in the indexing file: %s"
            % (OUTPUTFILE))
        print("\nWriting to file: %s"
            % (list_file))

        dataset = read_indexing_file(OUTPUTFILE)
        sorted_list = sort_list_of_tuples(sorting_option, dataset)

        ticker = 0  # Keep count of the number of entries.
        entries = []
        for item in sorted_list:
            ticker = ticker + 1
            entries.append("\n" + item[1] + "\t" + item[0])


        for entry in entries:
            append_to_file(entry, list_file)

        print("\nDone! Total %i entries written to %s"
            % (ticker, list_file))

# Not a valid option.
    else:
        print("\nDid not recognise the option: %s. Exiting program."
            % (option))
        sys.exit()




# Notes:
# print(datetime.fromtimestamp(os.path.getmtime(result)).strftime("%d%b%Y %H:%M:%S"))