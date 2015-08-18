Indexing of files for CD/DVD/HDD or other.



### Discdex versions
v0.0.8 (current)

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
3. Run as shell script "./discdex.py" in a terminal.



### Usage
Pre-launch: make sure the filetypes you want to index are specified in the config-part of discdex.py, youse wildcard * to index all files.

1. Go to the home folder of discdex in a terminal and run as shell script "./discdex.py".
2. Follow menu instructions.
3. Let the work be done by discdex!


#### SQL and using the .csv file exported by Discdex
An example of the SQL query to create the table in a MySQL database is as follows:

```SQL
USE dbteknik;

CREATE  TABLE IF NOT EXISTS `mydb`.`Discdex`
(
    `id` INT NOT NULL AUTO_INCREMENT ,
    `path_to_device` VARCHAR(255) NULL ,
    `device_name` VARCHAR(255) NULL ,
    `path_to_file` VARCHAR(255) NULL ,
    `file_name` VARCHAR(255) NULL ,
    `file_type` VARCHAR(255) NULL ,
    `modified` BIGINT NULL ,
    `size` BIGINT NULL ,
    PRIMARY KEY (`id`)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;
```

Then load the data into the table from the .csv file which Discdex generated.

```SQL
LOAD DATA INFILE '/path/to/your/csv/file/model.csv'
INTO TABLE mydb.Discdex
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
 (
    `path_to_device`,
    `device_name`,
    `path_to_file`,
    `file_name`,
    `file_type`,
    `modified`,
    `size`
);
```

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
    - Sort alphabetically
    - Sort alphabetically, group by device name.

* Export indexing as .CSV (Comma Separated Values) file for easy porting to databases.

Specs and options:

* Easy file type filter parameters in config.



### Bugs, known Issues and missing Features:

Please report an issue if one is found.

Functionality:

* Extract metadata from multimedia files. Needs to import module like Hachoir which can read metadata of various files. Interesting data could be:
	- Duration
	- Encoding/codec
	- Bitrate


Specs and options:

* A choice of the file metadata to include in the indexing system.
* When using wildcard "*" to index all file endings the filecount for each respective ending come across is not reported to user. One solution is a key-value pair ticker counter in the "walk_device" function.

Security: none

Code, style and performance: none



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
Credits go to docs.python.org, stackoverflow.com

How to use hachoir metadata parser:
https://github.com/jgstew/file-meta-data

Source code for hachoir:
https://bitbucket.org/haypo/hachoir/wiki/hachoir-metadata


