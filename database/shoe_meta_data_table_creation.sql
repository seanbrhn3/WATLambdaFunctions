-- create database shoe_data;

drop table if exists `shoe_data`.`shoe_meta_data`; create  table `shoe_data`.`shoe_meta_data`(
	uuid varchar(100),
    name varchar(100),
    price int,
    brand varchar(100),
    link varchar(100)
);