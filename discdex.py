#!/usr/bin/env python3

import glob, os
filetypes = "mp3 avi mpeg"
path = "/home/bizles/python" 
#input('Path to disc (ex. /media/bizles/SMALLBITS): ')
title = input('Name of disc (ex. disc_01): ')
outputFile = "test.txt"
ticker = 0


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


print ("Fisting files and folders under: " + path + " and writing to indexing file...")

for filetype in filetypes.split(" "):
    globlisting = path + '/*/*.' + filetype
    results = glob.glob(globlisting)
    ticker = ticker + len(results)
    
    print ("Found " + str(len(results)) + " files with ending: " + filetype)

    for name in results:
        #print ('\t', name)
        print ('\t' + os.path.basename(name))
        entry = "\n" + os.path.basename(name) + ' ' + title
        discdexIt(entry, outputFile)

print ("Total " + str(ticker) + " files written to " + outputFile)

