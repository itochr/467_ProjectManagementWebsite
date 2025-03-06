-- CS467 Capstone DDL Queries
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
taskProject INT NOT NULL,
taskSubject VARCHAR(50),
PRIMARY KEY (taskID),
FOREIGN KEY (taskAssignee) REFERENCES Accounts(accountID)
	ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (taskStatus) REFERENCES Statuses(statusID)
	ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (taskSprint) REFERENCES Sprints(sprintID)
	ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (taskProject) REFERENCES Projects(projectID)
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
accountTeamID INT NOT NULL,
accountRole VARCHAR(50),
-- accountTasksAssigned VARCHAR(50),
PRIMARY KEY (accountID),
FOREIGN KEY (accountTeamID) REFERENCES AccountTeams(accountTeamID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- Create AccountTeams Table
DROP TABLE IF EXISTS AccountsTeams;
DROP TABLE IF EXISTS AccountTeams;
CREATE TABLE AccountTeams (
accountTeamID INT NOT NULL AUTO_INCREMENT,
accountTeamName VARCHAR(50),
PRIMARY KEY (accountTeamID)
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
sprintName VARCHAR(50),
sprintStart DATE NOT NULL,
sprintEnd DATE NOT NULL,
accountTeamID INT NOT NULL,
PRIMARY KEY (sprintID),
FOREIGN KEY (accountTeamID) REFERENCES AccountTeams(accountTeamID)
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
projectName VARCHAR(50) NOT NULL,
projectStart DATE NOT NULL,
projectEnd DATE NOT NULL,
accountTeamID INT,
projectStatus INT NOT NULL,
PRIMARY KEY (projectID),
FOREIGN KEY (projectStatus) REFERENCES Statuses(statusID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (accountTeamID) REFERENCES AccountTeams(accountTeamID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- INSERT SAMPLE DATA INTO ACCOUNTTEAMS
INSERT INTO AccountTeams (accountTeamName) VALUES
('TeamA'),
('TeamB'),
('TeamC'),
('TeamD');

-- INSERT SAMPLE DATA INTO ACCOUNTS
INSERT INTO Accounts (accountUsername, accountFirstName, accountLastName, accountPassword, accountTeamID, accountRole) VALUES
  ('sastryv', 'Vish', 'Sastry','password', '1', 'Developer'),
  ('itoc', 'Christine', 'Ito','password', '2', 'Developer'),
  ('tsaor', 'Robert', 'Tsao','password', '3', 'Developer'),
  ('caiz', 'Zhiwei', 'Cai','password', '4', 'Developer'),
  ('staylor', 'Taylor', 'Swift', 'password', '1', 'Developer'),
  ('ldemi', 'Demi', 'Lovato', 'password', '1', 'Developer'),
  ('hwhitney', 'Whitney', 'Houston', 'password', '1', 'Developer'),
  ('swill', 'Will', 'Smith', 'password', '1', 'Developer'),
  ('mmarilyn', 'Marilyn', 'Monroe', 'password', '2', 'Developer'),
  ('htom', 'Tom', 'Hanks', 'password', '2', 'Developer'),
  ('jhugh', 'Hugh', 'Jackman', 'password', '2', 'Developer'),
  ('rryan', 'Ryan', 'Reynolds', 'password', '2', 'Developer'),
  ('hchris', 'Chris', 'Hemsworth', 'password', '3', 'Developer'),
  ('wamy', 'Amy', 'Winehouse', 'password', '3', 'Developer'),
  ('wemma', 'Emma', 'Watson', 'password', '3', 'Developer'),
  ('bkristen', 'Kristen', 'Bell', 'password', '3', 'Developer'),
  ('gariana', 'Ariana', 'Grande', 'password', '4', 'Developer'),
  ('fwill', 'Will', 'Ferrell', 'password', '4', 'Developer'),
  ('fcarrie', 'Carrie', 'Fisher', 'password', '4', 'Developer'),
  ('cwinston', 'Winston', 'Churchill', 'password', '4', 'Developer');

-- INSERT SAMPLE DATA INTO STATUSES
INSERT INTO Statuses (statusName) VALUES
('Backlog'), ('In Progress'), ('Completed');

-- INSERT SAMPLE DATA INTO PROJECTS
INSERT INTO Projects (projectName, projectStart, projectEnd, accountTeamID, projectStatus) VALUES
('ProjectA','2025-01-01','2025-02-01','1','1'),
('ProjectB','2025-02-02','2025-03-01','1','1'),
('ProjectC','2025-03-06','2025-04-01','1','1'),
('ProjectD','2025-04-07','2025-05-01','2','1'),
('ProjectE','2025-05-09','2025-06-01','2','1'),
('ProjectF','2025-06-10','2025-07-01','2','1'),
('ProjectG','2025-07-12','2025-08-01','3','1'),
('ProjectH','2025-08-13','2025-09-01','3','1'),
('ProjectI','2025-09-14','2025-10-01','3','1'),
('ProjectJ','2025-10-16','2025-11-01','4','1'),
('ProjectK', '2025-11-17','2025-12-01','4','1'),
('ProjectL', '2025-12-19','2026-01-01','4','1');

-- INSERT SAMPLE DATA INTO SPRINTS
INSERT INTO Sprints (sprintName, sprintStart, sprintEnd, accountTeamID) VALUES
('Sprint Alpha', '2025-01-01', '2025-02-01','1'),
('Sprint Beta', '2024-03-01', '2024-04-01','1'),
('Sprint Gamma', '2025-05-01', '2025-06-1','2'),
('Sprint Delta', '2025-07-01', '2025-08-01','2'),
('Sprint Epsilon', '2025-09-01', '2025-10-01','3'),
('Sprint Theta', '2025-11-01', '2025-12-01','3'),
('Sprint Iota', '2025-09-02', '2025-09-25','4'),
('Sprint Kappa', '2025-11-02', '2025-12-25','4');

-- INSERT SAMPLE DATA INTO TASKS
INSERT INTO Tasks (taskAssignee, taskAssigned, taskDue, taskStatus, taskSprint, taskProject, taskSubject) VALUES
('1','2025-01-01','2025-02-01','1','1','1','TaskDescription1'),
('1','2025-02-02','2025-03-01','2','1','1','TaskDescription2'),
('1','2025-03-06','2025-04-01','3','1','1','TaskDescription3'),
('2','2025-04-07','2025-05-01','1','3','4','TaskDescription4'),
('2','2025-05-09','2025-06-01','2','3','4','TaskDescription5'),
('2','2025-06-10','2025-07-01','3','3','4','TaskDescription6'),
('3','2025-07-12','2025-08-01','1','5','7','TaskDescription7'),
('3','2025-08-13','2025-09-01','2','5','7','TaskDescription8'),
('3','2025-09-14','2025-10-01','3','5','7','TaskDescription9'),
('4','2025-10-16','2025-11-01','1','7','10','TaskDescription10'),
('4','2025-11-17','2025-12-01','2','7','10','TaskDescription11'),
('4','2025-12-19','2026-01-01','3','7','10','TaskDescription12');

-- INSERT SAMPLE DATA INTO ACCOUNTTASKS (M:M)
INSERT INTO AccountTasks (accountID, taskID) VALUES
((SELECT accountID FROM Accounts WHERE accountLastName = 'Ito'), 1),
((SELECT accountID FROM Accounts WHERE accountLastName = 'Sastry'), 2);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;