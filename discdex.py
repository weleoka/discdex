#!/usr/bin/env python3

import re, os, fnmatch



"""
Config and options
"""
#FILETYPES = "avi mpeg mpg mov mp4 wmv"
FILETYPES = "*"
OUTPUTFILE = "discdex.txt"



"""
Append to indexing file.
The open() function is used with the "a" for append argument.

parameters:
    entry: string. An entry with file metadata to append to the indexing file
    destination: string. the indexing file to append the information to.

return:
    void
"""
def append_to_index_file(entry, destination):

    with open(destination, "a") as myfile:
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

    print ("Found %s files with ending: %s"
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
        basename = os.path.basename(result)

        if current_file_type == '*':
            file_type = (re.split('\.', basename))[-1]  # This is so that a file type can be assigned to the current entry.
        else:
            file_type = current_file_type

        name = re.split('.' + file_type, basename)[0]

        path_and_name_to_file = re.split(path_to_device, result)[1]

        try:
            path_to_file = re.split(name, path_and_name_to_file)[0]
        except:
            path_to_file = 'ERROR: bad character range'
            print ("\n Problem with name of file: %s "
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

# print datetime.fromtimestamp(os.path.getmtime(result)).strftime("%d%b%Y %H:%M:%S")



"""
MAIN
"""
if __name__ == '__main__': # simultaneously importable module and executable script

    ticker = 0  # Keep count of the total files found matching the filetype criteria.

    #path_to_device = input('Path to disc (ex. /media/simoni/superCD ): ')
    path_to_device = "/home/bunnybook/python/discdex" # Un-comment to have a fixed path location to work from.
    device_name = input('Your name for the device (ex. disc_01): ')

    print ("Listing files and folders under: %s and writing to indexing file..."
        % (path_to_device))

    for filetype in FILETYPES.split(" "):
        results = walk_device(path_to_device, filetype)
        entries = create_indexing_entry(results, filetype, path_to_device, device_name)

        ticker = ticker + len(entries)

        for entry in entries:
            append_to_index_file(entry, OUTPUTFILE)


    print ("Total %i files written to %s"
        % (ticker, OUTPUTFILE))

