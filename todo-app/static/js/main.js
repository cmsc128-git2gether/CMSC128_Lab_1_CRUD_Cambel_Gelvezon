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

// delete task function
// For Deleting a Task
const deleteModal = document.getElementById("deleteConfirmModal");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const cancelDeleteBtn = document.getElementById("cancel-delete-btn");
const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
let taskIdDelete = null;
let taskElementDelete = null;

// Toast / undo elements
const undoToast = document.getElementById("undoToast");
const undoToastMessage = document.getElementById("undoToastMessage");
const undoBtn = document.getElementById("undoBtn");

let undoTaskId = null;
let undoElement = null;
let undoParent = null;
let undoNextSibling = null;
let undoTimeoutId = null;

function openDeleteModal() {
    deleteModal.classList.add("show");
}

function closeDeleteModalView() {
    deleteModal.classList.remove("show");
    taskIdDelete = null;
    taskElementDelete = null;
}

document.querySelectorAll(".delete-btn").forEach(function (button) {
    button.addEventListener("click", function () {
        taskIdDelete = this.dataset.taskId;
        taskElementDelete = this.closest(".task-item");
        openDeleteModal();
    });
});

if (closeDeleteModal) {
    closeDeleteModal.addEventListener("click", closeDeleteModalView);
}

if (cancelDeleteBtn) {
    cancelDeleteBtn.addEventListener("click", closeDeleteModalView);
}

if (deleteModal) {
    deleteModal.addEventListener("click", function (event) {
        if (event.target === deleteModal) {
            closeDeleteModalView();
        }
    });
}
function showUndoToast(taskId, element, parent, nextSibling) {
    if (undoTimeoutId) {
        clearTimeout(undoTimeoutId);
        undoTaskId = null;
        undoElement = null;
    }

    undoTaskId = taskId;
    undoElement = element;
    undoParent = parent;
    undoNextSibling = nextSibling;

    undoToastMessage.textContent = "Task deleted";
    undoToast.classList.add("show");

    undoTimeoutId = setTimeout(function () {
        undoToast.classList.remove("show");
        undoTaskId = null;
        undoElement = null;
        undoTimeoutId = null;
    }, 5000);
}

if (undoBtn) {
    undoBtn.addEventListener("click", function () {
        if (!undoTaskId) return;

        clearTimeout(undoTimeoutId);
        undoTimeoutId = null;

        fetch(`/restore/${undoTaskId}`, { method: "POST" })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Failed to restore task (status " + response.status + ")");
                }
                // put the task element back where it was
                if (undoParent) {
                    undoParent.insertBefore(undoElement, undoNextSibling);
                }
            })
            .catch(function (error) {
                console.error("Error restoring task:", error);
                alert("Could not undo the delete. Please refresh the page.");
            })
            .finally(function () {
                undoToast.classList.remove("show");
                undoTaskId = null;
                undoElement = null;
            });
    });
}
if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener("click", function () {
        if (!taskIdDelete) return;

        const idToDelete = taskIdDelete;
        const elementToDelete = taskElementDelete;

        // capture position BEFORE removing anything
        const parentBeforeRemoval = elementToDelete ? elementToDelete.parentNode : null;
        const nextSiblingBeforeRemoval = elementToDelete ? elementToDelete.nextSibling : null;

        fetch(`/delete/${idToDelete}`, { method: "DELETE" })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Failed to delete task (status " + response.status + ")");
                }
                if (elementToDelete) {
                    elementToDelete.remove();
                    showUndoToast(idToDelete, elementToDelete, parentBeforeRemoval, nextSiblingBeforeRemoval);
                }
            })
            .catch(function (error) {
                console.error("Error deleting task:", error);
                alert("Could not delete the task. Please try again.");
            })
            .finally(function () {
                closeDeleteModalView();
            });
    });
}