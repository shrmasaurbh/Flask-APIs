from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)


@app.route('/reset-form',endpoint='reset via form')
def upload_file():
   return render_template('new_password.html')



	
		
if __name__ == '__main__':
   app.run(debug = True,port = 5001)