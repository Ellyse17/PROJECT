from flask import Flask,render_template,redirect,url_for,request,flash
app =Flask(__name__)
app.secret_key ='super_secret_key'
7
8
9
10
11
12
13
14
#Route to handle form submission
@app.route('/submit',methods=['POST'])
def submit_form():#Process form data
#Assuming form data is processed successfully
flash('Form submitted successfully!',category:'success')return redirect(url_for('home'))
#Route for the home page
15
16
@app.route('/')
def home():
17
return render_template('index.html')
18
19
20
if __name__=='__main__':
app.run(debug=True)
21


