from flask import Flask, render_template, request, redirect, url_for
import re
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/movie'
db = SQLAlchemy(app)

class Contact_us(db.Model):
    '''
    sno, name email, msg
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(120), nullable=False)

class Booking(db.Model):
    '''
    sno, name email, msg
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    movie = db.Column(db.String(20), nullable=False)
    seat = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

MOVIE_DICT = {
    'Avengers': {'seats': 'Gold', 'time': '010800 12:00'},
    'SpiderMan': {'seats': 'Gold', 'time': '010800 12:00'},
    'KGF 2': {'seats': 'Gold', 'time': '010800 12:00'}
}

SEAT_TYPES = ['Gold', 'Standard', 'FronTier Gold']

@app.route('/')
def index():
    return render_template('index.html', movie_dict=MOVIE_DICT)

@app.route('/contact_us', methods = ['GET', 'POST'])  
def contact_us():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('msg')
        entry = Contact_us(name=name, email = email, msg = message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact_us.html')

@app.route('/book', methods=['GET','POST'])
def book():
    movie_name =  request.form.get('movie')
    seat_type =  request.form.get('seat')
    time_slot =  request.form.get('time')

    print("Movie: {}, Seat Type: {}, Time Slot: {}".format(movie_name, seat_type, time_slot))

    if movie_name in MOVIE_DICT and seat_type in SEAT_TYPES and re.match('\d{6} \d{2}:\d{2}', time_slot):
        print("Redirecting to booking_successful.html")
        return render_template('booking_successful.html', movie_name=movie_name, seat_type=seat_type, time_slot=time_slot)
    else:
        print("Redirecting to index.html")
        return redirect(url_for('index'))
    
@app.route('/booking', methods=['GET','POST'])
def booking():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        movie = request.form.get('movie')
        seat = request.form.get('seat')
        time = request.form.get('time')
        entry = Booking(name=name, email = email, movie = movie,seat = seat,time = time)
        db.session.add(entry)
        db.session.commit()
    return render_template('booking_successful.html',movie_name=movie, seat_type=seat, time_slot=time)

@app.route('/About', methods=['GET','POST'])
def About():
    return render_template('about_us.html')
 
if __name__ == '__main__':
    app.run(debug=True)