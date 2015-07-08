Indexing for CD/DVD/HDD or other.



### Discdex versions
v0.0.1 (current)

(Note to author: version specified in readme.md, changelog.md, and git.)


### Requirements
Python 3.4

A NIX based system ( This is due to the fact that MS-Windows path using backslash needs to be escaped in the code to work).


### Overview
A simple tool to create a log of all files and folders on a removable media device such as a CD or BLU-Ray. The log appends an arbitary name to all files/folders which specifies which removable media entity it can be found on.

Discdex aims to collect metadata on all, or choice, data stored on removable storage devices. The metadata can then be put to use for organising, be searched through and ultimately data can be kept track of more easily.


### Installation


### Usage
Enter path to disc to be indexed. Next enter a name/label of your choice for referencing that particular disc. 


### Current Features:
General functinality:

* Walks a directory (recursive) and its subdirectories and records all files found that match the fileType criteria.
* Saves information on
	- Name
	- File type
	- Location disc name
	- Full path to file
	- Size
	- Date modified



Specs and options:

* Easy file type parameters.

### Known Issues/Missing Features:
Functionality:

* Needs to check the supplied path for validity.
* Missing feature to extract metadata from multimedia files. Needs to import module like Hachoir which can read metadata of various files. Interesting data could be:
	- Duration
	- Encoding/codec
	- Bitrate

Specs and options:

* A choice of the file metadata to include in the indexing system.

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
LICENCE.md for details.

Copyright (c) 2015 A.K. Weeks


### Sources, inspiration and notes
Credits go to docs.python.org, stack-overflow.com,


