from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
db = SQLAlchemy(app)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task >'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_id = request.form['id']
        task_q1 = request.form['q1']
        task_q2 = request.form['q2']
        task_q3 = request.form['q3']
        password = request.form['password']
        if password == '123':
        	tasks = Rating.query.order_by(Rating.date_created).all()
        	return render_template('display.html', tasks = tasks)
        else:
        	new_add = Rating(id=task_id, q1=task_q1, q2=task_q2, q3=task_q3)
        #new_id = Rating(q1=task_id)
        #new_q2 = Rating(q2=task_q2)
        #new_q3 = Rating(q3=task_q3)

        	try:
       			db.session.add(new_add)
        		db.session.commit()
        		return render_template('thanks.html')
        	except:
        		return 'There was an issue adding ur task enter correct user id'

    else:
        #tasks = Rating.query.order_by(Rating.date_created).all()
        return render_template('index.html')


#@app.route('/', methods=['POST', 'GET'])
#def display():
#	if request.method == "POST":
#		password = request.form['password']
#		if(password=='123'):
#			try:
#				tasks1 = Rating.query.order_by(Rating.date_created).all()
#       			return render_template('display.html', tasks1=tasks1)
#         	except:
#        		return "error displaying"
#
#        else:
#        	return "wrong password"

#    else:
#        return render_template('index.html')



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Rating.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        tasks = Rating.query.order_by(Rating.date_created).all()
        return render_template('display.html', tasks = tasks)
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Rating.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)