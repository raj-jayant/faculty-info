// static/script.js

// Function to handle the teacher status change
document.addEventListener('DOMContentLoaded', function() {
    // Teacher dashboard specific functionality
    const statusSelect = document.querySelector('select[name="status"]');
    const roomNumberInput = document.querySelector('input[name="room_number"]');

    if (statusSelect && roomNumberInput) {
        statusSelect.addEventListener('change', function() {
            if (this.value === 'absent') {
                roomNumberInput.disabled = true;
                roomNumberInput.value = '';
            } else {
                roomNumberInput.disabled = false;
            }
        });
    }

    // Admin dashboard specific functionality
    const roleSelect = document.querySelector('select[name="role"]');
    const teacherNameInput = document.querySelector('.teacher-name');

    if (roleSelect && teacherNameInput) {
        roleSelect.addEventListener('change', function() {
            if (this.value === 'teacher') {
                teacherNameInput.style.display = 'block';
                teacherNameInput.required = true;
            } else {
                teacherNameInput.style.display = 'none';
                teacherNameInput.required = false;
            }
        });
    }
});

// Function to filter teachers in student dashboard
function filterTeachers() {
    const select = document.getElementById('teacherSelect');
    const selectedTeacher = select.value.toLowerCase();
    const rows = document.getElementsByClassName('teacher-row');

    for (let row of rows) {
        const teacherName = row.getElementsByTagName('td')[0].textContent.toLowerCase();
        if (selectedTeacher === '' || teacherName === selectedTeacher) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    }
}

// Auto-refresh student dashboard every 30 seconds
if (window.location.pathname.includes('student_dashboard')) {
    setInterval(function() {
        location.reload();
    }, 30000);
}

// Confirm user deletion
function confirmDelete(userId) {
    return confirm('Are you sure you want to delete this user?');
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    event.preventDefault();
                    alert('Please fill in all required fields');
                    field.focus();
                }
            });
        });
    });
});