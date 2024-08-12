from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# Configuring SQLite database with Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the model
class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    em_phone_number = db.Column(db.String(15), nullable=False)
    house_number = db.Column(db.String(10), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()
   
@app.route('/', methods=['POST', 'GET'])
def add_details():
    if request.method == 'POST':
        new_data = ContactInfo(
            full_name=request.form['full_name'],
            email_address=request.form['email_address'],
            phone_number=request.form['phone_number'],
            em_phone_number=request.form['em_phone_number'],
            house_number=request.form['house_number']
        )
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('success'))
    
    return render_template('index.html')

@app.route('/success')
def success():
    all_data = ContactInfo.query.all()
    return render_template('view.html', data=all_data)

# Exporting to pandas
@app.teardown_appcontext
def export_data_on_close(exception=None):
    data = ContactInfo.query.all()
    data_list = [item.__dict__ for item in data]
    for item in data_list:
        item.pop('_sa_instance_state', None)
    df = pd.DataFrame(data_list)
    
    df = df.rename(columns={
        'full_name': 'Full Name',
        'email_address': 'Email Address',
        'phone_number': 'Phone Number',
        'em_phone_number': 'Emergency Phone Number',
        'house_number': 'House Number',
    })

    # Reorder columns to ensure 'id' is the first column
    df = df[['id', 'Full Name', 'Email Address', 'Phone Number', 'Emergency Phone Number', 'House Number']]
    
    # Export to CSV
    df.to_csv('output.csv', index=False)

if __name__ == '__main__':
    app.run(debug=True, port=9000)
