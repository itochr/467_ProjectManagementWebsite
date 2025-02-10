-- CS467 Capstone Data Manipulation Queries
-- Winter Quarter 2025
-- : used to denote values that will contain variables readable by Flask


-- Accounts table CRUD operations
SELECT Accounts.accountID, Accounts.accountUsername, Accounts.accountFirstName, Accounts.accountLastName, Accounts.accountPassword, Accounts.accountTeam, Accounts.accountRole
    FROM Accounts;

INSERT INTO Accounts (accountUsername, accountFirstName, accountLastName, accountPassword, accountTeam, accountRole)
VALUES (:usernameInput, :accountFirstName, :accountLastName, :accountPassword, :accountTeam, :accountRole);

-- do update later

DELETE FROM Accounts WHERE Accounts.accountUsername = :usernameInput;



-- AccountTasks table CRUD operations (M:M intersection table)



-- Tasks table CRUD operations



-- Sprints table CRUD operations
SELECT Sprints.sprintID, Sprints.sprintProject, Sprints.sprintStart, Sprints.sprintEnd
FROM Sprints;

INSERT INTO Sprints (sprintProject, sprintStart, sprintEnd)
VALUES (:sprintProject, :sprintStart, :sprintEnd);

--update Sprints- user enters ID of sprint they want to edit, then they can update project, start, and end
UPDATE Sprints 
SET sprintProject = :sprintProjectInput, sprintStart = :sprintStartInput, sprintEnd = :sprintEndInput
WHERE sprintID = :sprintIDInput;

DELETE FROM Sprints WHERE Sprints.sprintID = :sprintInput;


-- Projects table CRUD operations
SELECT Projects.projectID, Projects.projectStart, Projects.projectEnd
FROM Projects;

INSERT INTO Projects (projectStart, projectEnd)
VALUES (:projectStart, :projectEnd);


-- Statuses table CRUD operations
INSERT INTO Statuses (statusName) VALUES (:statusNameInput);
SELECT statusID, statusName FROM Statuses;
UPDATE Statuses SET statusName = :statusNameInput WHERE statusID = :statusIDInput; --have user enter statusID in order to edit or delete existing statusName;
DELETE FROM Statuses Statuses WHERE statusID = :statusIDInput;

