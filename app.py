#importing all neccessary libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#initiating the Flask App
app=Flask(__name__)

#declare the secret key for the application
app.secret_key="Secret Key"

#database connection part
#the database has 2 tables - data(for employees),todo(for notes)
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#initializing the database
db=SQLAlchemy(app)

#instantiating the class for Employees Section
class Data(db.Model):
    #4 columns - id(Primary Key),name,email,department
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    department=db.Column(db.String(100))
    
    #initializing the variables
    def __init__(self,name,email,department):
        self.name=name
        self.email=email
        self.department=department 

#instantiating the class for Notes Section
class Todo(db.Model):
    #3 columns - id(Primary Key),title,complete
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    #initializing the variables
    def __init__(self,title,complete):
        self.title=title
        self.complete=complete
        
#Routing to the home page of application
@app.route('/')
def index():
    return render_template("index.html")

#Routing to the Employee Section of the application
@app.route('/e')
def employee():
    #retrieve data from the database table - "data"
    all_data=Data.query.all()
    return render_template("employees.html",employees=all_data)

#Routing to the Notes Section of the application
@app.route('/n')
def notes():
    #retrieve data from the database table - "todo"
    notes_list=Todo.query.all()
    return render_template("notes.html",notes_list=notes_list)

#Notes Section - Add Notes
@app.route("/addnotes",methods=['POST'])
def addtodo():
    if request.method == 'POST':
        #notes taken as input is stored in database
        title = request.form.get("title")
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('notes'))

#Notes Section - Delete Notes
@app.route("/deletenotes/<id>",methods=['GET','POST'])
def deletetodo(id):
    #notes deleted from database
    todo=Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('notes'))

#Employee Section - Insert Employee Details
@app.route('/insert',methods=['POST'])
def insert():
    if request.method == 'POST':
        #employee details taken as input is stored in database
        name=request.form['name']
        email=request.form['email']
        department=request.form['department']
        #store all the data in a variable
        mydata=Data(name=name,email=email,department=department)
        db.session.add(mydata)
        db.session.commit()
        return redirect(url_for('employee'))

#Employee Section - Update Employee Details
@app.route('/update', methods=['GET','POST'])
def update():
    if request.method=='POST':
        #employee details taken as input is updated in database
        my_data=Data.query.get(request.form.get('id'))
        my_data.name=request.form['name']
        my_data.email=request.form['email']
        my_data.department=request.form['department']
        db.session.commit()
        return redirect(url_for('employee'))

#Employee Section - Delete Employee Details
@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    #employee detail is deleted from database
    my_data=Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('employee'))

#initialize the application and execute it
if __name__=="__main__":
    app.run(debug=True)
