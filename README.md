Indexing of files for CD/DVD/HDD or other.



### Discdex versions
v0.0.4 (current)

(Note to author: version specified in readme.md, changelog.md, and git.)



### Requirements
Python 3.4

A NIX based system ( This is due to the fact that MS-Windows path using backslash needs to be escaped in the code to work).



### Overview
A simple tool to create a log of all files and folders on a removable media device such as a CD, BLU-Ray or thumb-drive. This indexer can append a user supplied arbitary name to all files/folders which specifies which removable media entity it can be found on.

Discdex aims to collect metadata on all, or choice, data stored on removable storage devices. The metadata can then be put to use for organising and easily be searched through. Ultimately data can be kept track of more easily with discdex.

The default files scanned for are: avi mpeg mov mp4 wmv
This can easily be changed in the config part of discdex.py

An entry in the indexing file takes the form:

Path to device - Device name - Path to file - File name - File type - Modified - Size



### Installation
1. Git clone or download archive and extract.
2. Make discdex.py executable
3. Run as bash script "./discdex.py"



### Usage
Pre-launch: make sure the filetypes you want to index are specified in the config-part of discdex.py.

1. Enter path to disc to be indexed at prompt.
2. Enter a name/label of your choice for referencing that particular disc.
3. Let the work be done by discdex!



### Current Features:
General functinality:

* Walk a directory (recursive) and its subdirectories and record file metadata.
* Checks if path is valid before scanning.
* Checks to see if the indexing file exists - then creates it or appends to it.
* Filter files on file type or wildcard(*) search - indexing of all file types.
* Save information on
    - Path to device (supplied by user at prompt)
    - Location device name (supplied by user at prompt)
    - Path to file
    - Name of file
    - File type
    - Date modified
    - Size

* Make a human readable list of all the entries in the indexing file.

Specs and options:

* Easy file type filter parameters in config.



### Known Issues/Missing Features:
Functionality:

* Missing feature to extract metadata from multimedia files. Needs to import module like Hachoir which can read metadata of various files. Interesting data could be:
	- Duration
	- Encoding/codec
	- Bitrate
* Cannot sort alphabetically and group by device yet.

Specs and options:

* A choice of the file metadata to include in the indexing system.
* When using wildcard "*" to index all file endings the filecount for each respective ending come across is not reported to user. One solution is a key-value pair ticker counter in the "walk_device" function.


Security: none


Code, style and performance: none



### Bugs and Issues
Please report an issue if one is found.



### Contributing
If you'd like to contribute to Discdex's development, start by forking the GitHub repo:

https://github.com/weleoka/discdex.git

Have a look at the known issues and missing features and take a pick or find something else that needs doing.

The best way to get your changes merged is as follows:

1. Clone your fork
2. Hack away
3. If you are adding significant new functionality, document it in the README
4. Do not change the version number, I will do that on my end
5. Push the repo up to GitHub
6. Send a pull request to [weleoka/discdex](https://github.com/weleoka/discdex)



### Licence

GNU GENERAL PUBLIC LICENSE

LICENCE.md for details.

Copyright (c) 2015 A.K. Weeks



### Sources, inspiration and notes
Credits go to docs.python.org, stack-overflow.com

How to use hachoir metadata parser:
https://github.com/jgstew/file-meta-data

Source code for hachoir:
https://bitbucket.org/haypo/hachoir/wiki/hachoir-metadata


