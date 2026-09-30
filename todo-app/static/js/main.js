// JS Functions

// For New Task Modal
const taskModal = document.getElementById("taskModal");
const newTaskBtn = document.getElementById("newTaskBtn");
const closeTaskModal = document.getElementById("closeTaskModal");
const cancelTask = document.getElementById("cancelTask");

// Open modal
function openTaskModal() {
    taskModal.classList.add("show");
}

// Close modal
function closeTaskModalView() {
    taskModal.classList.remove("show");
}

// New Task button
if (newTaskBtn) {
    newTaskBtn.addEventListener("click", openTaskModal);
}

// Close button
if (closeTaskModal) {
    closeTaskModal.addEventListener("click", closeTaskModalView);
}

// Cancel button
if (cancelTask) {
    cancelTask.addEventListener("click", closeTaskModalView);
}

// Close when clicking outside the modal
if (taskModal) {
    taskModal.addEventListener("click", function (event) {
        if (event.target === taskModal) {
            closeTaskModalView();
        }
    });
}

// For Editing Existing Task Modal
const editTaskModal = document.getElementById("editTaskModal");
const editTaskForm = document.getElementById("editTaskForm");
const closeEditBtn = document.getElementById("closeEditModal");
const cancelEditBtn = document.getElementById("cancelEdit");

// Get Exisiting Elements
document.querySelectorAll(".edit-btn").forEach(button => {
    button.addEventListener("click", function () {
        const id = this.dataset.taskId;
        document.getElementById("edit-title").value = this.dataset.title;
        document.getElementById("edit-due_date").value = this.dataset.dueDate;
        document.getElementById("edit-due_time").value = this.dataset.dueTime;
        document.querySelectorAll('input[name="priority"]').forEach(radio => {
            radio.checked = radio.value === (this.dataset.priority || "");
        });
        document.querySelectorAll('input[name="tag"]').forEach(radio => {
            radio.checked = radio.value === (this.dataset.tag || "");
        });

        editTaskForm.action = `/edit/${id}`;
        editTaskModal.classList.add("show");

    });
});

// Close Modal
function closeEditModal() {
    editTaskModal.classList.remove("show");
}

// Close Edit
if (closeEditBtn) {
    closeEditBtn.addEventListener("click", closeEditModal);
}

// Cancel Edit
if (cancelEditBtn) {
    cancelEditBtn.addEventListener("click", closeEditModal);
}

// Edit
if (editTaskModal) {
    editTaskModal.addEventListener("click", function (event) {
        if (event.target === editTaskModal) {
            closeEditModal();
        }
    });
}

// ------------- LAB 2 FUNCTION ------------- //

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.auth-form');
    if (!form) return;

    form.noValidate = true;

    // show / hide password
    form.querySelectorAll('.toggle-password').forEach((button) => {
        const input = button.parentElement.querySelector('input');
        const icon = button.querySelector('i');

        button.addEventListener('click', () => {
            const showing = input.type === 'text';
            input.type = showing ? 'password' : 'text';
            icon.className = showing ? 'bi bi-eye' : 'bi bi-eye-slash';
            button.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
        });
    });

    // form validation
    const EMAIL_PATTERN = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    const isRegister = !!form.elements.confirm_password;

    // rules returns a message or ''
    const rules = {
        email(value) {
            if (!value.trim()) return 'Email is required.';
            if (!EMAIL_PATTERN.test(value.trim())) return 'Please enter a valid email address.';
            return '';
        },
        display_name(value) {
            return value.trim() ? '' : 'Display name is required.';
        },
        password(value) {
            if (!value) return 'Password is required.';
            const min = form.elements.password.minLength;
            if (isRegister && min > 0 && value.length < min) {
                return `Password must be at least ${min} characters.`;
            }
            return '';
        },
        confirm_password(value) {
            if (!value) return 'Please confirm your password.';
            if (value !== form.elements.password.value) return 'Passwords do not match.';
            return '';
        },
    };

    function showError(input, message) {
        const errorEl = input.closest('.field').querySelector('.field-error');
        errorEl.textContent = message;
        input.classList.toggle('invalid', message !== '');
        input.setAttribute('aria-invalid', message !== '');
    }

    function validateField(input) {
        const rule = rules[input.name];
        if (!rule) return '';
        const message = rule(input.value);
        showError(input, message);
        return message;
    }

    const fields = Array.from(form.querySelectorAll('input')).filter((i) => rules[i.name]);

    fields.forEach((input) => {
        // check when the user leaves a field
        input.addEventListener('blur', () => validateField(input));

        // recheck sintantly as they fix it
        input.addEventListener('input', () => {
            if (input.classList.contains('invalid')) validateField(input);

            // changing the password can fix or break the confirm field
            if (input.name === 'password' && form.elements.confirm_password?.value) {
                validateField(form.elements.confirm_password);
            }
        });
    });

    // block the submit if anything is invalid
    form.addEventListener('submit', (event) => {
        let firstInvalid = null;

        fields.forEach((input) => {
            if (validateField(input) && !firstInvalid) firstInvalid = input;
        });

        if (firstInvalid) {
            event.preventDefault();
            firstInvalid.focus();
        }
    });
});