CREATE DATABASE IF NOT EXISTS `desafio`;
USE `desafio`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) UNIQUE NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`pronomes` varchar(100) NOT NULL,
    `genero` varchar (12) NOT NULL,
    PRIMARY KEY (`id`)
);
