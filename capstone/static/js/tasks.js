// document.addEventListener("DOMContentLoaded", function(event) {

// 	});


window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
};

function openCreateModal() {
    document.getElementById('addTaskDiv').style.display = 'block';
}

function showProjectDetails(project) {
    console.log('Project:', project);

    document.getElementById('projectDetailsModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function confirmDelete() {
    if (confirm('Are you sure you want to delete this project?')) {
        const projectID = document.getElementById('projectID').value;
        document.getElementById('deleteProjectID').value = projectID;
        document.getElementById('deleteForm').submit();
    }
}

function divClick() {
    alert('Hey');
}

function showHide(elementID) {
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


document.getElementById("myButton").addEventListener("click", function() {
    this.style.backgroundColor = "red"; // Changes background color to red on click
    this.style.color = "white"; // Changes text color
});