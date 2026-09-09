#temporary for testing 
#not yet connected to database 
tasks = []

next_id = 1

# Adding a task
def add_task(title, due_date, due_time, priority, tag):
    global next_id
    
    task = {
        'id': next_id,
        'title': title,
        'due_date': due_date,
        'due_time': due_time,
        'priority': priority,
        'tag': tag,
        'completed': False
    }
    
    tasks.append(task)
    next_id += 1
    
    return tasks

# Get all task
def get_all_tasks():
    return tasks

# Get task
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    
    return None

# Update after editing
def update_task(task_id, title, due_date, due_time, priority, tag):
    task = get_task(task_id)
    
    if task is None:
        return False
    
    task['title'] = title
    task['due_date'] = due_date
    task['due_time'] = due_time
    task['priority'] = priority
    task['tag'] = tag
    
    return True

# Delete 
def delete_task(task_id):
    task = get_task(task_id)
    
    if task is None:
        return False
    
    tasks.remove(task)
    
    return True

# Complete
def complete_task(task_id):
    task = get_task(task_id)
    
    if task is None:
        return False
    
    task['completed'] = True
    return True