#!/usr/bin/env python3 

import re, os, fnmatch



"""
Config and options
"""
FILETYPES = "avi mpeg mov mp4 wmv"
OUTPUTFILE = "discdex.txt"



"""
Append to indexing file. 
The open() function is used with the "a" for append argument.

parameters:
    batch: An batch of entries to append to the file
    destination: the file to append the information to.

return:
    void
"""
def append_to_index_file(batch, destination):

    with open(destination, "a") as myfile:
        myfile.write(batch)
        myfile.close()



"""
Walk the device's directory tree and add files matching the criteria to list.

parameters:
    path: string. Root path to work from.
    filetype: string. The file types to list.
    
return:
    list
"""
def walk_device(path, filetype):

    results = []
    
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.' + filetype):
            results.append(os.path.join(root, filename))

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
    currentFiletype: string. The current filetype being listed.
    pathToDevice: string. The path to the currently indexed storage device.
    
return:
    entries: list. All the files with their stats as string.
"""
def create_indexing_entry(results, currentFiletype, pathToDevice):
    entries = []

    for result in results:
        name = re.split('.' + currentFiletype, os.path.basename(result))[0]
        pathAndNameToFile = re.split(pathToDevice, result)[1]

        try:
            pathToFile = re.split(name, pathAndNameToFile)[0]
        except:
            pathToFile = 'ERROR: bad character range'
            print ("\n Problem with name of file: %s " 
                % (pathAndNameToFile))
            pass

        #print ('\t' + name)
        
        entries.append('\n'
            + pathToDevice + '\t' 
            + sourceName  + '\t'                    # Device name
            + pathToFile + '\t'                     # Path to file
            + name + '\t'                           # Name of file
            + currentFiletype + '\t'                # File type
            + str(os.path.getmtime(result)) + '\t'  # Date modified
            + str(os.path.getsize(result)) + '\t'   # Size
            )
    return entries

# print datetime.fromtimestamp(os.path.getmtime(result)).strftime("%d%b%Y %H:%M:%S")



"""
MAIN
"""
if __name__ == '__main__': # simultaneously importable module and executable script

    ticker = 0  # Keep count of the total files found matching the filetype criteria.

    path = input('Path to disc (ex. /media/simoni/superCD ): ')
    # path = "/home/deppi/python/discdex" # Un-comment to have a fixed path location to work from.
    sourceName = input('Your name for the device (ex. disc_01): ')

    print ("Listing files and folders under: %s and writing to indexing file..." 
        % (path))

    for filetype in FILETYPES.split(" "):
        results = walk_device(path, filetype)
        entries = create_indexing_entry(results, filetype, path)

        ticker = ticker + len(entries)

        for entry in entries:
            append_to_index(entry, OUTPUTFILE)


    print ("Total %i files written to %s"
        % (ticker, OUTPUTFILE))

