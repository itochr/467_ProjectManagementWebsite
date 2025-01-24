-- CS467 Capstone DDL Queries
-- Winter Quarter 2025

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- Create Tasks Table
DROP TABLE IF EXISTS Tasks;
CREATE TABLE Tasks (
taskID INT(10) NOT NULL AUTO_INCREMENT,
taskAssignee VARCHAR(50) NOT NULL,
taskAssigned DATE NOT NULL,
taskDue date NOT NULL,
taskStatus VARCHAR(50) NOT NULL,
taskType VARCHAR(50) NOT NULL,
PRIMARY KEY (taskID)
);

-- Create Accounts Table
DROP TABLE IF EXISTS Accounts;
CREATE TABLE Accounts (
accountID INT(10) NOT NULL AUTO_INCREMENT,
accountUsername VARCHAR(50) NOT NULL,
accountFirstName VARCHAR(50) NOT NULL,
accountLastName VARCHAR(50) NOT NULL,
accountPassword VARCHAR(50) NOT NULL,
accountTeam VARCHAR(50),
accountRole VARCHAR(50),
accountTasksAssigned VARCHAR(50),
PRIMARY KEY (accountID)
);

DROP TABLE IF EXISTS Sprints;
CREATE TABLE Sprints (
sprintID INT(10) NOT NULL AUTO_INCREMENT,
sprintStart DATE NOT NULL,
PRIMARY KEY (sprintID)
);

-- Create Status Table
DROP TABLE IF EXISTS Statuses;
CREATE TABLE Statuses (
statusID INT(10) NOT NULL AUTO_INCREMENT,
statusName VARCHAR(50) NOT NULL,
PRIMARY KEY (statusID)
);

-- Create Stories Table
DROP TABLE IF EXISTS Stories;
CREATE TABLE Stories (
storyID INT(10) NOT NULL AUTO_INCREMENT,
storyDescription VARCHAR(150),
PRIMARY KEY (storyID)
);
