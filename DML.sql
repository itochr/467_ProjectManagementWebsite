-- CS367 Capstone DML Queries
-- Winter Quarter 2025


-- User table CRUD operations



-- userTasks table CRUD operations (M:M intersection table)



-- Tasks table CRUD operations



-- Sprints table CRUD operations



-- Projects table CRUD operations



-- Statuses table CRUD operations
INSERT INTO Statuses (statusName) VALUES (:statusNameInput);
SELECT statusID, statusName FROM Statuses; 
UPDATE Statuses SET statusName = :statusNameInput WHERE statusID = :statusIDInput; --have user enter statusID in order to edit or delete existing statusName;
DELETE FROM Statuses Statuses WHERE statusID = :statusIDInput;

