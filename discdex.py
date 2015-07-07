#!/usr/bin/env python3

import os, fnmatch



"""
Config and options
"""
filetypes = "mp3 avi mpeg txt"
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
Walk the directory tree and log add files found to list.

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
Create string of file stats append to list.

parameters:
    results: list. All the files found.
    currentFiletype: string. The current filetype being listed.
    
return:
    entries: list. All the files with their stats as string.
"""
def entryIt(results, currentFiletype):
    entries = []

    for result in results:
        print ('\t' + os.path.basename(result))
        entries.append('\n' 
            + os.path.basename(result) + '\t' 
            + sourceName  + '\t' 
            + str(os.path.getsize(result)) + '\t'
            + currentFiletype)

    return entries




"""
MAIN
"""
ticker = 0

path = "/home/bizles/python/discdex/" 
#path = input('Path to disc (ex. /media/bizles/SMALLBITS): ')
sourceName = input('Name of disc (ex. disc_01): ')

print ("Listing files and folders under: " + path + " and writing to indexing file...")

for filetype in filetypes.split(" "):
    results = walkIt(path, filetype)
    entries = entryIt(results, filetype)

    ticker = ticker + len(entries)

    for entry in entries:
        discdexIt(entry, outputFile)


print ("Total " + str(ticker) + " files written to " + outputFile)

