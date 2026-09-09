from flask import Flask, render_template, request, redirect
# url_for
# from database import get_db_connection, init_db, add_task, get_task, get_all_tasks, update_task, delete_task, complete_task

from task_logic import (
    add_task,
    get_task,
    get_all_tasks,
    update_task,
    delete_task,
    complete_task
)

app = Flask(__name__)

# init_db()

@app.route('/')
def index():
    tasks = get_all_tasks()
    
    # takes you to the interface index.html
    return render_template('index.html',tasks = tasks)

# For adding tasks
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    due_date = request.form['due_date']
    due_time = request.form['due_time']
    priority = request.form['priority']
    tag = request.form['tag']

    
    add_task(
        title,
        due_date,
        due_time, 
        priority,
        tag
    )
    
    return redirect('/')
   

# For completing tasks
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    complete_task(task_id) 
    
    return redirect('/')

# For deleting tasks
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    delete_task(task_id) 
    
    return redirect('/')

# edit "getter"
@app.route('/edit/<int:task_id>')
def edit(task_id):
    task = get_task(task_id)
    
    if task is None:
        return redirect('/')
    
    # switch to editing view
    return render_template(
        '(name).html',
        task=task
    )

# edit and update values
@app.route('/edit/<int:task_id>', methods=['POST'])
def update(task_id):
    title = request.form['title']
    due_date = request.form['due_date']
    due_time = request.form['due_time']
    priority = request.form['priority']
    tag = request.form['tag']
    
    update_task(
        task_id,
        title,
        due_date,
        due_time,
        priority,
        tag
    )
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)   