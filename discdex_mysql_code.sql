USE dbteknik;

CREATE  TABLE IF NOT EXISTS `mydb`.`Discdex` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `path_to_device` VARCHAR(255) NULL ,
  `device_name` VARCHAR(255) NULL ,
  `path_to_file` VARCHAR(255) NULL ,
  `file_name` VARCHAR(255) NULL ,
  `file_suffix` VARCHAR(255) NULL ,
  `modified` BIGINT NULL ,
  `size` BIGINT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;
-- /path/to/your/csv/file/model.csv
DROP TABLE mydb.Discdex;
DELETE FROM mydb.Discdex;
USE mydb;
SELECT * FROM Discdex;

LOAD DATA INFILE '/home/bunnybook/python/discdex/example.csv'
INTO TABLE mydb.Discdex
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
 (
`path_to_device`,
`device_name`,
`path_to_file`,
`file_name`,
`file_suffix`,
`modified`, -- @var1
`size`);
-- SET modified = STR_TO_DATE(@var1,'%m/%d/%Y %k:%i');

