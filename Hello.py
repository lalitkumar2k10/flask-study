from flask import Flask,redirect, url_for,request,abort
from flask import render_template,make_response,session
from flask import flash
from flask_mail import Mail, Message

from werkzeug import secure_filename

app = Flask(__name__)

# filepath
# (instance_path='data/', instance_relative_config=True)

# mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lalit.kumar@prolitus.com'
app.config['MAIL_PASSWORD'] = 'titaniump'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/hello/<name>')
def hello_world(name):
	return 'Hello %s!' % name
#	return "Hello World"

@app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID

@app.route('/python/')
def hello_python():
	# calling url /python or /python/ return same instead 404 in one
   return 'Hello Python'
   
def helloworld():
	return 'hello world'

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      print('here')
      return redirect(url_for('hello_python'))
   else:
      return redirect(url_for('hello_world',name= name))



#form example
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      print("form",request,request.form)
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      print("for",request,request.args)
      return redirect(url_for('success',name = user))

@app.route('/html')
def index():
   return '<html><body><h1>Hello World</h1></body></html>'


@app.route('/template/<user>')
def index_template(user):
   mdict = {'phy':50,'che':60,'maths':70}
   return render_template('hello.html', name = user, marks=mdict)
 
@app.route("/js")
def index_js():
   return render_template("index_js.html")
 #send form data

@app.route('/student')
def student():
   return render_template('login_student.html')

@app.route('/result',methods = ['POST', 'GET'])
def index_res():
   if request.method == 'POST':
      result = request.form
      # mdict = {'phy':50,'che':60,'maths':70}
      # result submit and display
      # return render_template('hello_result.html',marks=result)
      
      # set cookie
      resp = make_response(render_template('readcookie.html'))
      resp.set_cookie('userID', result['nm'])
   
      return resp

@app.route('/login_session', methods = ['GET', 'POST'])
def login_session():
   if request.method == 'POST':
      session['username'] = request.form['username']
      return redirect(url_for('index_home'))
   return render_template('session_form.html')

@app.route('/home')
def index_home():
   if 'username' in session:
      username = session['username']
      return 'Logged in as ' + username + '<br>' + \
         "<b><a href = '/logout'>click here to log out</a></b>"
   return "You are not logged in <br><a href = '/login_session'></b>" + \
      "click here to log in</b></a>"
      
      
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index_home'))
      
@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome '+name+'</h1>'

@app.route('/r')
def index_r():
   return render_template('session_form_r.html')

@app.route('/login_r',methods = ['POST', 'GET'])
def login_r():
   if request.method == 'POST':
      if request.form['username'] == 'admin' :
         return redirect(url_for('success_r'))
      else:
         abort(401)
   else:
      return redirect(url_for('index_r'))

@app.route('/success_r')
def success_r():
   return 'logged in successfully'

# flash message
@app.route('/f')
def index_f():
   return render_template('index_f.html')

@app.route('/login_f', methods = ['GET', 'POST'])
def login_f():
   error = None
   
   if request.method == 'POST':
      if request.form['username'] != 'admin' or \
         request.form['password'] != 'admin':
         error = 'Invalid username or password. Please try again!'
      else:
         flash('You were successfully logged in')
         print('flashed!!')
         return redirect(url_for('index_f'))
			
   return render_template('login_f.html', error = error)

      
# file upload

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
		
# mail
@app.route("/m")
def index_m():
   msg = Message('Hello', sender = 'lalit.kumar@prolitus.com', recipients = ['lalitsharma2k10@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

# wt form
# from flask import Flask, render_template, request, flash
from forms import ContactForm
# app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
   form = ContactForm()
   
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('contact.html', form = form)
      else:
         return render_template('success.html')
   elif request.method == 'GET':
         return render_template('contact.html', form = form)

# database

import sqlite3 as sql
# app = Flask(__name__)

conn = sql.connect('database.db')
print("Opened database successfully")

# creater already
# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print("Table created successfully")
conn.close()


@app.route('/s')
def home_s():
   return render_template('home_s.html')

@app.route('/enternew')
def new_student():
   return render_template('student_s.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result_s.html",msg = msg)
         con.close()

@app.route('/list')
def list_s():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


#"
if __name__ == '__main__':
	# app.run(host, port, debug, options
	app.debug=True
	# below secret for session
	app.secret_key = 'any random string'
	# below not working
	app.add_url_rule('/', 'hi' , helloworld)
	app.run()