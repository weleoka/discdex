#!/usr/bin/env python3 

import re, os, fnmatch



"""
Config and options
"""
filetypes = "avi mpeg mov mp4 wmv"
outputFile = "discdex.txt"



"""
Append to indexing file. 
The open() function is used with the "a" for append argument.

parameters:
    batch: An batch of entries to append to the file
    destination: the file to append the information to.

return:
    void
"""
def discdexIt(batch, destination):

    with open(destination, "a") as myfile:
        myfile.write(batch)
        myfile.close()



"""
Walk the directory tree and add the files found to a list.

parameters:
    path: string. Root path to work from.
    filetypes: string. The file types to list.
    
return:
    list
"""
def walkIt(path, filetype):

    results = []
    
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.' + filetype):
            results.append(os.path.join(root, filename))

    print ("Found " + str(len(results)) + " files with ending: " + filetype)

    return results



"""
Create string of file metadata and append to list.
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
def entryIt(results, currentFiletype, pathToDevice):
    entries = []

    for result in results:
        name = re.split('.' + currentFiletype, os.path.basename(result))[0]
        pathAndNameToFile = re.split(pathToDevice, result)[1]

        try:
            pathToFile = re.split(name, pathAndNameToFile)[0]
        except:
            pathToFile = 'read-error: bad character range'
            print ("\n Problem with name of file: " + pathAndNameToFile)
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
ticker = 0

#path = "/home/deppi/python/discdex" 
path = input('Path to disc (ex. /media/bizles/SMALLBITS ): ')
sourceName = input('Your name for the disc (ex. disc_01): ')

print ("Listing files and folders under: " + path + " and writing to indexing file...")

for filetype in filetypes.split(" "):
    results = walkIt(path, filetype)
    entries = entryIt(results, filetype, path)

    ticker = ticker + len(entries)

    for entry in entries:
        discdexIt(entry, outputFile)


print ("Total " + str(ticker) + " files written to " + outputFile)

