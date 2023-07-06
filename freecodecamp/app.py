from flask import Flask, render_template, url_for, request 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True   #debug_quries

app.app_context().push()  #https://stackoverflow.com/questions/31444036/runtimeerror-working-outside-of-application-context

db = SQLAlchemy(app)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        print(task_content)
        new_task = Todo(content=task_content)
        print(new_task)
        try : 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding yout task'
    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

    # return render_template('index.html')

@app.route('/delete/<string:content>')
def delete(content):
    task_to_delete=Todo.query.get_or_404(content)
    try :
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem while deleting the task'

@app.route('/update/<string:content>', methods=['POST','GET'])
def update(content):
    task = Todo.query.get_or_404(content)

    if request.method == 'POST':
        pass
    else:
        return render_template('update.html', task)

if __name__ == "__main__":
    app.run(debug=True)
