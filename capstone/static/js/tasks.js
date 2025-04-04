window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
};

function openCreateModal() {
    document.getElementById('addTaskDiv').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function confirmDelete() {
    if (confirm('Are you sure you want to delete this task?')) {
        const taskID = document.getElementById('taskID').value;
        document.getElementById('deleteTaskID').value = taskID;
        document.getElementById('deleteForm').submit();
    }
}

function confirmDeleteAllTeamTasks() {
    if (confirm('Are you sure you want to delete ALL Team Tasks?')) {
        document.getElementById('deleteTeamTasksForm').submit();
    }
}

function confirmDeleteAllUserTasks() {
    if (confirm('Are you sure you want to delete ALL User Tasks?')) {
        document.getElementById('deleteUserTasksForm').submit();
    }
}

function showTaskDetails(task) {
    document.getElementById('taskID').value = task.taskID;
    document.getElementById('editTaskSubject').value = task.taskSubject;
    document.getElementById('editTaskDescription').value = task.taskDescription;
    const formattedStartDate = formatDate(task.taskAssigned);
    const formattedEndDate = formatDate(task.taskDue);
    document.getElementById('editTaskAssigned').value = formattedStartDate;
    document.getElementById('editTaskDue').value = formattedEndDate;
    const statusSelect = document.getElementById('editTaskStatus');
    for (let i = 0; i < statusSelect.options.length; i++) {
        if (statusSelect.options[i].value == task.taskStatus) {
            statusSelect.selectedIndex = i;
            break;
        }
    }
    const teamMemberSelect = document.getElementById('editTaskAssignee');
    for (let i = 0; i < teamMemberSelect.options.length; i++) {
        if (teamMemberSelect.options[i].value == task.accountID) {
            teamMemberSelect.selectedIndex = i;
            break;
        }
    }
    const sprintSelect = document.getElementById('editTaskSprint');
    for (let i = 0; i < sprintSelect.options.length; i++) {
        if (sprintSelect.options[i].value == task.sprintID) {
            sprintSelect.selectedIndex = i;
            break;
        }
    }
    const projectSelect = document.getElementById('editTaskProject');
    for (let i = 0; i < projectSelect.options.length; i++) {
        if (projectSelect.options[i].value == task.projectID) {
            projectSelect.selectedIndex = i;
            break;
        }
    }
    document.getElementById('taskDetailsModal').style.display = 'block';
}

function formatDate(dateString) {
    if (!dateString) return ""; // Handle null or undefined
    let dateObj = new Date(dateString);
    if (isNaN(dateObj.getTime())) {
        console.error("Invalid date:", dateString);
        return ""; // Invalid date, return empty string
    }
    const mysqlDate = dateObj.toISOString().split('T')[0];
    return mysqlDate;
}

function toggleShowHide(elementID) {
	var x = document.getElementById(elementID);
	if (x.style.display === "none") {
	  x.style.display = "block";
	} else {
	  x.style.display = "none";
	}
  }

function showHide2() {
var x = document.getElementById("hideButton2");
if (x.style.display === "none") {
	x.style.display = "block";
} else {
	x.style.display = "none";
}
}

function showTeamTasks() {
    var x = document.getElementsByClassName("teamTasks-div");
    var y = document.getElementsByClassName("userTasks-div");
    for (var i = 0; i < x.length; i++) {
        x[i].style.display = 'block';
    }
    for (var i = 0; i < y.length; i++) {
    y[i].style.display = 'none';
    }
}

function showUserTasks() {
    var x = document.getElementsByClassName("teamTasks-div");
    var y = document.getElementsByClassName("userTasks-div");
    for (var i = 0; i < x.length; i++) {
        x[i].style.display = 'none';
    }
    for (var i = 0; i < y.length; i++) {
    y[i].style.display = 'block';
    }
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
    event.stopPropagation();
}

function allowDrop(event) {
    event.preventDefault();
}

function drop(event) {
    event.preventDefault();
    const taskID = event.dataTransfer.getData("text");
    const projectCard = document.getElementById(taskID);
    // Find the closest status-column div
    const column = event.target.closest('.status-column');
    if (column) {
        const columnContent = column.querySelector('.column-content');
        columnContent.appendChild(projectCard);
        // Get the new task status from the column's data-status attribute
        const newStatusName = column.getAttribute('data-status');
        const newStatusID = column.getAttribute('data-status-id');
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/updateTaskStatus");
        xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
        const body = JSON.stringify({
            taskID: taskID,
            taskStatus: newStatusID
        });
        xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 201) {
            console.log(JSON.parse(xhr.responseText));
        } else {
            console.log(`Error: ${xhr.status}`);
        }
        };
        xhr.send(body);
    }
}