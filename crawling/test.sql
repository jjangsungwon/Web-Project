CREATE DATABASE testDB default CHARACTER SET UTF8;

use testDB;

CREATE TABLE department(
	idx     INT UNSIGNED NOT NULL PRIMARY KEY,
	Title   VARCHAR(256)NOT NULL,
    Date    VARCHAR(256)NOT NULL,
    Link	VARCHAR(256)NOT NULL
) CHARSET=utf8;

CREATE TABLE Recruitment(
	idx     INT UNSIGNED NOT NULL PRIMARY KEY,
	Title   VARCHAR(256)NOT NULL,
    Date    VARCHAR(256)NOT NULL,
    Link	VARCHAR(256)NOT NULL
) CHARSET=utf8;

select * from department;
select * from Recruitment;
