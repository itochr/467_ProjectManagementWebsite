-- CS367 Capstone DDL Queries
-- Winter Quarter 2025

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;
USE defaultdb;

-- Create Tasks Table
DROP TABLE IF EXISTS Tasks;
CREATE TABLE Tasks (
taskID INT NOT NULL AUTO_INCREMENT,
taskAssignee INT NOT NULL, 
taskAssigned DATE NOT NULL, 
taskDue DATE NOT NULL, 
taskStatus INT NOT NULL, 
taskSprint INT NOT NULL,
taskType VARCHAR(50), 
PRIMARY KEY (taskID),
FOREIGN KEY (taskAssignee) REFERENCES Accounts(accountID)
	ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (taskStatus) REFERENCES Statuses(statusID)
	ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (taskSprint) REFERENCES Sprints(sprintID)
	ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- Create Accounts Table
DROP TABLE IF EXISTS Accounts;
CREATE TABLE Accounts (
accountID INT NOT NULL AUTO_INCREMENT,
accountUsername VARCHAR(50) NOT NULL, 
accountFirstName VARCHAR(50) NOT NULL, 
accountLastName VARCHAR(50) NOT NULL, 
accountPassword VARCHAR(50) NOT NULL, 
accountTeam VARCHAR(50),
accountRole VARCHAR(50),
accountTasksAssigned VARCHAR(50),
PRIMARY KEY (accountID)
);

-- Create AccountTasks Table (M:M)
DROP TABLE IF EXISTS AccountTasks;
CREATE TABLE AccountTasks (
accountTaskID INT NOT NULL AUTO_INCREMENT,
accountID INT NOT NULL, 
taskID INT NOT NULL, 
PRIMARY KEY (accountTaskID),
FOREIGN KEY (accountID) REFERENCES Accounts(accountID)
	ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (taskID) REFERENCES Tasks(taskID)
	ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- CREATE Sprints Table
DROP TABLE IF EXISTS Sprints;
CREATE TABLE Sprints (
sprintID INT NOT NULL AUTO_INCREMENT,
sprintProject INT NOT NULL,
sprintStart DATE NOT NULL,
sprintEnd DATE NOT NULL,
PRIMARY KEY (sprintID),
FOREIGN KEY (sprintProject) REFERENCES Projects(projectID)
	ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- Create Statuses Table
DROP TABLE IF EXISTS Statuses;
CREATE TABLE Statuses (
statusID INT NOT NULL AUTO_INCREMENT,
statusName VARCHAR(50) NOT NULL,
PRIMARY KEY (statusID)
);

-- Create Projects Table
DROP TABLE IF EXISTS Projects;
CREATE TABLE Projects (
projectID INT NOT NULL AUTO_INCREMENT,
projectStart DATE NOT NULL, 
projectEnd DATE NOT NULL, 
PRIMARY KEY (projectID)
);
