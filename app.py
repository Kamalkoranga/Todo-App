from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.title

db.create_all()

@app.route('/')
def home():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['GET', 'POST'])
def add():
    title = request.form.get('title')
    print(title)
    description = request.form.get('description')
    new_todo = Todo(title = title, description = description, is_completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))
    

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter(Todo.id==todo_id).first()
    todo.is_completed = True
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('home'))


# EDIT PAGE

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    if request.method == 'POST':
        todo = Todo.query.filter(Todo.id == todo_id).first()
        print(todo)
        title = request.form['title']
        desciption = request.form['description']
        todo.title = title
        todo.description = desciption
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('home'))
    todo = Todo.query.filter(Todo.id == todo_id).first()
    return render_template('edit.html', todo=todo)


@app.route('/delete/<todo_id>')
def delete(todo_id):
    todo = Todo.query.filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)