from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

app.secret_key = 'your_very_secret_key'

users_db = {}

with open('model_and_symptoms_list.pkl', 'rb') as file:
    model, symptom_names = pickle.load(file)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' not in session:
        flash('You must sign in to book a consultation.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        flash('Slot booked successfully, appointment details sent to entered phone number and email.')
        return redirect(url_for('index'))  
    return render_template('booking.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_db and users_db[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password', 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users_db[username] = password  
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('predict.html')

symptoms_list_df = pd.read_excel('symptom_list.xlsx')
known_symptoms = symptoms_list_df['Symptoms'].tolist()

@app.route('/predict', methods=['POST'])
def predict_disease():
    data = request.json
    input_symptoms = data['symptoms']
    
    input_df = pd.DataFrame(np.zeros((1, len(symptom_names))), columns=symptom_names)
    
    for symptom in input_symptoms:
        if symptom in symptom_names:
            input_df.at[0, symptom] = 1

    prediction = model.predict(input_df)
    
    return jsonify({'prediction': prediction[0]})

@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    symptoms_df = pd.read_excel('symptom_list.xlsx')
    symptoms_list = symptoms_df['Symptoms'].tolist()
    return jsonify(symptoms_list)

@app.route('/result_page')
def result_page():
    return render_template('result_page.html')

@app.route('/consult')
def consult():
    return render_template('consult.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run(debug=True)

CORS(app)
