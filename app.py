from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")
    new_task = Todo(name=name, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/updatepriority/<int:todo_id>')
def updatep(todo_id):
    todo = Todo.query.get(todo_id)
    todo.priority = not todo.priority
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/deleteall')
def deleteall():
    Todo.query.delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/edit/<int:todo_id>/<string:newname>')
def edit(todo_id, newname):
    todo = Todo.query.get(todo_id)
    todo.name = newname
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/sort')
def sort():
    todo_list = Todo.query.order_by(Todo.priority).all()
    db.session.commit()
    # return render_template('base.html', todo_list=todo_list)

if __name__ == '__main__':
    app.run(debug=True)

# this was made by meeeeeeeeeeeeeeeeeeeeeeee