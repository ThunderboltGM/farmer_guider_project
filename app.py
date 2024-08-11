from flask import Flask,url_for,request,render_template

import pandas as pd

import joblib

import sqlite3

df = pd.read_csv('./models/filteringdata.csv')

kms = joblib.load('./models/KMeans.lb')

std = joblib.load('./models/standardScaler.lb')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cropResult',methods=['POST','GET'])
def cropResult():
    if request.method == 'POST':
        nitrogen = int(request.form['nitrogen'])
        phosphorus = int(request.form['phosphorus'])
        pottasium = int(request.form['pottasium'])
        temperature = int(request.form['temperature'])
        humidity = int(request.form['humidity'])
        ph = int(request.form['ph'])
        rainfall = int(request.form['rainfall'])

        data = [nitrogen,phosphorus,pottasium,temperature,humidity,ph,rainfall]

        final_data = std.transform([data])
        prediction = kms.predict(final_data)[0]

        df2 = df[df['cluster_no'] == prediction]

        final_result = list(df2['label'].unique())

        if prediction == 0:
            image_path = [
                ('/images/maize.jpeg','MAIZE'),
                ('/images/pigeonpeas.jpeg','PIGEONPEAS'),
                ('/images/mothbeans.jpeg','MOTHBEANS'),
                ('/images/mungbeans.jpeg','MUNGBEANS'),
                ('/images/blackgram.jpeg','BLACKGRAM'),
                ('/images/lentil.jpeg','LENTIL'),
                ('/images/mango.jpeg','MANGO'),
                ('/images/orange.jpeg','ORANGE'),
                ('/images/papaya.jpeg','PAPAYA')
                ]

        elif prediction == 1:
            image_path = [
                ('/images/pigeonpeas.jpeg','PIGEONPEAS'),
                ('/images/mothbeans.jpeg','MOTHBEANS'),
                ('/images/mango.jpeg','MANGO')
                ]

        elif prediction == 2:
            image_path = [
                ('images/grapes.jpeg','GRAPES'),
                ('images/apple.jpeg','APPLE')
                ]

        elif prediction == 3:
            image_path = [
                ('/images/pomogranate.jpeg','POMOGRANATE'),
                ('/images/orange.jpeg','ORANGE'),
                ('/images/papaya.jpeg','PAPAYA'),
                ('/images/coconut.jpeg','COCONUT')
                ]

        elif prediction == 4:
            image_path = [
                ('images/rice.jpeg','RICE'),
                ('images/pigeonpeas.jpeg','PIGEONPEAS'),
                ('images/papaya.jpeg','PAPAYA'),
                ('images/coconut.jpeg','COCONUT'),
                ('images/jute.jpeg','JUTE'),
                ('images/coffee.jpeg','COFFEE')
                ]

        elif prediction == 5:
            image_path = [
            ('/images/maize.jpeg','MAIZE'),
            ('/images/banana.jpeg','BANANA'),
            ('/images/watermelon.jpeg','WATERMELON'),
            ('/images/muskmelon.jpeg','MUSKMELON'),
            ('/images/papaya.jpeg','PAPAYA'),
            ('/images/cotton.jpeg','COTTON'),
            ('/images/coffee.jpeg','COFFEE')
            ]

        elif prediction == 6:
            image_path = [
            ('/images/maize.jpeg','MAIZE'),
            ('/images/chickpea.jpeg','CHICKPEAS'),
            ('/images/kidneybeans.jpeg','KIDNEYBEANS'),
            ('/images/pigeonpeas.jpeg','PIGEONPEAS'),
            ('/images/lentil.jpeg','LENTIL')
            ]

        elif prediction == 7:
            image_path = [
                ('/images/chickpea.jpeg','CHICKPEAS')
                ]

        return render_template('result.html',imagePath = image_path)

@app.route('/contactForm',methods=['POST','GET'])
def contactForm():
    if request.method == 'POST':
        conn = sqlite3.connect('customerData.db')
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        customerData = (name,email,message)
        insertionQuerry = """
        insert into customerData values(?,?,?)
        """
        cur = conn.cursor()
        cur.execute(insertionQuerry,customerData)
        print('data inserted in database successfully')
        conn.commit()
        cur.close()
        conn.close()
        return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)