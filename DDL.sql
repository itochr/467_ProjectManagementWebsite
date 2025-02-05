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
-- accountTasksAssigned VARCHAR(50),
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

-- INSERT SAMPLE DATA INTO ACCOUNTS
INSERT INTO Accounts (accountUsername, accountFirstName, accountLastName, accountPassword, accountTeam, accountRole) VALUES
  ('sastryv', 'Vish', 'Sastry','password', 'TeamA', 'Developer'),
  ('itoc', 'Christine', 'Ito','password', 'TeamB', 'Developer'),
  ('tsaor', 'Robert', 'Tsao','password', 'TeamC', 'Developer'),
  ('caiz', 'Zhiwei', 'Cai','password', 'TeamD', 'Developer');

-- INSERT SAMPLE DATA INTO STATUSES
INSERT INTO Statuses (statusName) VALUES
('Backlog'), ('In progress'), ('Completed');

-- INSERT SAMPLE DATA INTO PROJECTS
INSERT INTO Projects (projectStart, projectEnd) VALUES
('2024-10-01', '2024-12-31'),
('2025-01-01', '2025-04-01');

-- INSERT SAMPLE DATA INTO SPRINTS
INSERT INTO Sprints (sprintProject, sprintStart, sprintEnd) VALUES
((SELECT projectID FROM Projects WHERE projectStart = '2025-01-01'), '2025-02-01', '2025-02-28'),
((SELECT projectID FROM Projects WHERE projectStart = '2024-10-01'), '2024-10-01', '2024-12-31');

-- INSERT SAMPLE DATA INTO TASKS
INSERT INTO Tasks (taskAssignee, taskAssigned, taskDue, taskStatus, taskSprint, taskType) VALUES
((SELECT accountID FROM Accounts WHERE accountLastName = 'Ito'), '2025-02-02', '2025-02-10', (SELECT statusID FROM Statuses WHERE statusName = 'In progress'), (SELECT sprintID FROM Sprints WHERE sprintStart = '2025-02-01'), 'Testing1'),
((SELECT accountID FROM Accounts WHERE accountLastName = 'Sastry'), '2024-12-01', '2025-12-31', (SELECT statusID FROM Statuses WHERE statusName = 'Completed'), (SELECT sprintID FROM Sprints WHERE sprintStart = '2024-10-01'), 'Testing2');

-- INSERT SAMPLE DATA INTO ACCOUNTTASKS (M:M)
INSERT INTO AccountTasks (accountID, taskID) VALUES
((SELECT accountID FROM Accounts WHERE accountLastName = 'Ito'), 1),
((SELECT accountID FROM Accounts WHERE accountLastName = 'Sastry'), 2);

--  ((SELECT accountID FROM Accounts WHERE accountLastName = 'Ito'), (SELECT taskID FROM Tasks WHERE taskType = 'Testing1')),
--  ((SELECT accountID FROM Accounts WHERE accountLastName = 'Sastry'), SELECT taskID FROM Tasks WHERE taskType = 'Testing2');

SET FOREIGN_KEY_CHECKS=1;
COMMIT;