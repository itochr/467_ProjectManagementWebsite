-- CS467 Capstone Data Manipulation Queries
-- Winter Quarter 2025
-- : used to denote values that will contain variables readable by Flask


-- Accounts table CRUD operations------------------------------------------------------------------------------------
SELECT Accounts.accountID, Accounts.accountUsername, Accounts.accountFirstName, Accounts.accountLastName, Accounts.accountPassword, Accounts.accountTeamName as Team, Accounts.accountRole
FROM Accounts
INNER JOIN AccountTeams ON AccountTeams.accountTeamID = Accounts.accountTeam; --matches the team name in Accounts to team name in Teams and returns the Name, not the ID

--user enters team name, and query matches it with the ID from AccountTeams to enter into table
INSERT INTO Accounts (accountUsername, accountFirstName, accountLastName, accountPassword, (SELECT accountTeamID FROM AccountTeams WHERE :teamInput = AccountTeams.accountTeamName), accountRole)
VALUES (:usernameInput, :accountFirstName, :accountLastName, :accountPassword, :accountTeam, :accountRole);

--user enters Team Name and query matches it to the ID in AccountTeams
UPDATE Accounts
SET Accounts.accountUsername = :usernameInput, Accounts.accountFirstName = :firstNameInput, Accounts.accountLastName = :lastNameInput, Accounts.accountPassword = :passwordInput, Accounts.accountTeam = (SELECT accountTeamID FROM AccountTeams WHERE :teamInput = AccountTeams.accountTeamName), Accounts.accountRole = :roleInput
WHERE accountID = :accountIDInput;

DELETE FROM Accounts WHERE Accounts.accountUsername = :usernameInput;


--AccountTeams CRUD operations-----------------------------------------------------------------------------------
SELECT AccountTeams.accountTeamID, AccountTeams.accountTeamName
FROM AccountTeams;

INSERT INTo AccountTeams (accountTeamName)
VALUES (:accountTeamNameInput);

--user enters teamID to delete or update
DELETE FROM AccountTeams WHERE AccountTeams.accountTeamID = :teamIDInput;

UPDATE AccountTeams
SET AccountTeams.accountTeamName = :accountTeamNameInput
WHERE AccountTeams.accountTeamID = :teamIDInput;


-- AccountTasks table CRUD operations (M:M intersection table)--------------------------------------------------------





-- Tasks table CRUD operations-------------------------------------------------------------------------------------



-- Sprints table CRUD operations--------------------------------------------------------------------------------------
SELECT Sprints.sprintID, Sprints.sprintProject, Sprints.sprintStart, Sprints.sprintEnd
FROM Sprints;

INSERT INTO Sprints (sprintProject, sprintStart, sprintEnd)
VALUES ((SELECT projectID FROM Projects WHERE :projectInput = Projects.projectStart), :sprintStart, :sprintEnd);

--update Sprints- user enters ID of sprint they want to edit, then they can update project, start, and end
UPDATE Sprints 
SET sprintProject = :sprintProjectInput, sprintStart = :sprintStartInput, sprintEnd = :sprintEndInput
WHERE sprintID = :sprintIDInput;

DELETE FROM Sprints WHERE Sprints.sprintID = :sprintInput;


-- Projects table CRUD operations------------------------------------------------------------------------------
SELECT Projects.projectID, Projects.projectName, Projects.projectStart, Projects.projectEnd
FROM Projects;

INSERT INTO Projects (projectName, projectStart, projectEnd)
VALUES (:projectStart, :projectEnd);

-- user enters ID of project they want to edit, then they can update start and end dates
UPDATE Projects 
SET projectStart = :projectStartInput, projectEnd = :projectEndInput 
WHERE projectID = :projectIDInput;
DELETE FROM Projects WHERE Projects.projectID = :projectIDInput


-- Statuses table CRUD operations----------------------------------------------------------------------------------
INSERT INTO Statuses (statusName) VALUES (:statusNameInput);
SELECT statusID, statusName FROM Statuses;
UPDATE Statuses SET statusName = :statusNameInput WHERE statusID = :statusIDInput; --have user enter statusID in order to edit or delete existing statusName;
DELETE FROM Statuses Statuses WHERE statusID = :statusIDInput;

