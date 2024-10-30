function showForm() {
    const formDiv = document.getElementById("add-student-form");
    if (formDiv.style.display === "none" || formDiv.style.display === "") {
        formDiv.style.display = "block";
    } else {
        formDiv.style.display = "none";
    }
}

function addStudent() {
    const form = document.getElementById('studentForm');
    const formData = new FormData(form);

    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/add_student/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken  
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Student added successfully");
            location.reload();
        } else {
            alert("Failed to add student");
        }
    })
    .catch(error => console.error("Error:", error));
}
function enableEditing(studentId) {
    document.getElementById(`subject-${studentId}`).disabled = false;
    document.getElementById(`marks-${studentId}`).disabled = false;
    document.getElementById(`edit-button-${studentId}`).form.submit();
}
