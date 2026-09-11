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
    editTaskModal.addEventListener("click", function(event) {
        if (event.target === editTaskModal) {
            closeEditModal();
        }
    });
}

