DROP DATABASE IF EXISTS scis_upskilling;

CREATE DATABASE scis_upskilling;
USE scis_upskilling;

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
    `account_id` INT AUTO_INCREMENT NOT NULL,
    `account_name` VARCHAR(20) NOT NULL,
    
     PRIMARY KEY (`account_id`)
);
