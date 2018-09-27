-- NIH.sql --
-- Author: Jun Yen Leung --

-- Remake Database --
DROP DATABASE `NIH`;
CREATE DATABASE IF NOT EXISTS `NIH`;
USE `NIH`;

-- Create Tables --
CREATE TABLE `Movies` ( 
	`Title` VarChar( 255 ),
	`Text` MEDIUMBLOB);