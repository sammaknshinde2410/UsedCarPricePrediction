from flask import Flask,render_template,jsonify,request, redirect, url_for, session
import joblib
import numpy as np
import pandas as pd
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re




app = Flask(__name__)
app.config['SECRET_KEY'] ='secret'
model = joblib.load(open('MLProject\Application\gb_newcarmodel.joblib','rb'))


# Set up the MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sammak'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'ucpp'
mysql = MySQL(app)



# testing ml model using an api
@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    new_data = np.array(list(data.values())).reshape(-1,43)
    output = model.predict(new_data)
    return jsonify(output[0])





# User login form and Authentication
@app.route('/',methods=['GET','POST'])
def login():
    prompt =''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s',[email,password])
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['username'] = user['username']
            session['email'] = user['email']
            return render_template('home.html')
        else:
            prompt = 'Please Enter Valid Credentials! '
    return render_template('login.html',prompt = prompt)
    
# User logout
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    session.pop('email',None)
    return redirect(url_for('login'))



# New User registration and Authentication
@app.route('/register', methods =['GET','POST'])
def register():
    prompt=''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s',(email,))
        account = cursor.fetchone()
        if account:
            prompt = 'Account Already Exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            prompt = 'Invalid email address!'
        elif not username or not password or not email:
            prompt = 'Please fill the form!'
        else:
            cursor.execute('INSERT INTO users VALUES(%s,%s,%s)',(username, email, password))
            mysql.connection.commit()
            prompt = 'User Sucessfully Registered!'
            return render_template('login.html',prompt = prompt)
    elif request.method == 'POST':
        prompt='Please fill the form!'
    return render_template('register.html',prompt=prompt)



#defining a home page accesible only to the registered users
@app.route("/home")
def home():
    prompt = ''
    if 'email' not in session:
        prompt = 'Please log in to access this page.'
        return render_template('login.html', prompt=prompt)
    return render_template('home.html')



@app.route("/prediction-form")
def form():
    prompt = ''
    if 'email' not in session:
        prompt = 'Please log in to access this page.'
        return render_template('login.html', prompt=prompt)
    return render_template('prediction.html')
    

@app.route("/predict",methods=['GET','POST'])
def predict():
    manufacturer = request.form['manufacturer']
    k_driven = float(request.form['kms_driven'])
    mileage = float(request.form['mileage'])
    engine = float(request.form['engine'])
    power = float(request.form['power'])
    seats = int(request.form['seats'])
    age = float(request.form['age'])
    fuel_type = request.form['fuel_type']
    transmission = request.form['transmission']
    owner_type = request.form['owner_type']
    email = session.get('email')
    username = session.get('username')

    
    # Convert the categorical variables to numerical values
    fuel_type_petrol = 1 if fuel_type == 'Petrol' else 0
    fuel_type_diesel = 1 if fuel_type == 'Diesel' else 0
    fuel_type_lpg = 1 if fuel_type == "LPG" else 0
    fuel_type_electric = 1 if fuel_type == "Electric" else 0
    fuel_type_cng = 1 if fuel_type == 'CNG' else 0
    transmission_manual = 1 if transmission == 'Manual' else 0
    owner_type_third = 1 if owner_type == 'Third' else 0
    owner_type_fourth_above = 1 if owner_type == 'Fourth & Above' else 0
    owner_type_second = 1 if owner_type == 'Second' else 0
    owner_type_first = 1 if owner_type == 'First' else 0
    manufacturer_audi = 1 if manufacturer == 'Audi' else 0
    manufacturer_bmw = 1 if manufacturer == 'BMW' else 0
    manufacturer_bentley = 1 if manufacturer == 'Bentley' else 0
    manufacturer_chevrolet = 1 if manufacturer == 'Chevrolet' else 0
    manufacturer_datsun = 1 if manufacturer == 'Datsun' else 0
    manufacturer_fiat = 1 if manufacturer == 'Fiat' else 0
    manufacturer_force = 1 if manufacturer == 'Force' else 0
    manufacturer_ford = 1 if manufacturer == 'Ford' else 0
    manufacturer_honda = 1 if manufacturer == 'Honda' else 0
    manufacturer_hyundai = 1 if manufacturer == 'Hyundai' else 0
    manufacturer_isuzu = 1 if manufacturer == 'Isuzu' else 0
    manufacturer_jaguar = 1 if manufacturer == 'Jaguar' else 0
    manufacturer_jeep = 1 if manufacturer == 'Jeep' else 0
    manufacturer_lamborghini = 1 if manufacturer == 'Lamborghini' else 0
    manufacturer_land = 1 if manufacturer == 'Land' else 0
    manufacturer_mahindra = 1 if manufacturer == 'Mahindra' else 0
    manufacturer_maruti = 1 if manufacturer == 'Maruti' else 0
    manufacturer_mercedes = 1 if manufacturer == 'Mercedes_Benz' else 0
    manufacturer_mini = 1 if manufacturer == 'Mini' else 0
    manufacturer_mitsubishi = 1 if manufacturer == 'Mitsubishi' else 0
    manufacturer_nissan = 1 if manufacturer == 'Nissan' else 0
    manufacturer_porsche = 1 if manufacturer == 'Porsche' else 0
    manufacturer_renault = 1 if manufacturer == 'Renault' else 0
    manufacturer_skoda = 1 if manufacturer == 'Skoda' else 0
    manufacturer_smart = 1 if manufacturer == 'Smart' else 0
    manufacturer_tata = 1 if manufacturer == 'Tata' else 0
    manufacturer_toyota = 1 if manufacturer == 'Toyota' else 0
    manufacturer_volkswagen = 1 if manufacturer == 'Volkswagen' else 0
    manufacturer_volvo = 1 if manufacturer == 'Volvo' else 0


    # Create a new dataframe with the input values
    data = pd.DataFrame({'Kilometers_Driven': [k_driven],
                         'Mileage': [mileage],
                         'Engine': [engine],
                         'Power': [power],
                         'Seats': [seats],
                         'Age': [age],
                         'Fuel_Type_Diesel': [fuel_type_diesel],
                         'Fuel_Type_Electric': [fuel_type_electric],
                         'Fuel_Type_LPG': [fuel_type_lpg],
                         'Fuel_Type_Petrol': [fuel_type_petrol],
                         'Transmission_Manual': [transmission_manual],
                         'Owner_Type_Fourth & Above': [owner_type_fourth_above],
                         'Owner_Type_Second': [owner_type_second],
                         'Owner_Type_Third': [owner_type_third],
                         'Manufacturer_Audi': [manufacturer_audi],
                         'Manufacturer_BMW': [manufacturer_bmw],
                         'Manufacturer_Bentley': [manufacturer_bentley],
                         'Manufacturer_Chevrolet': [manufacturer_chevrolet],
                         'Manufacturer_Datsun': [manufacturer_datsun],
                         'Manufacturer_Fiat': [manufacturer_fiat],
                         'Manufacturer_Force': [manufacturer_force],
                         'Manufacturer_Ford': [manufacturer_ford],
                         'Manufacturer_Honda': [manufacturer_honda],
                         'Manufacturer_Hyundai': [manufacturer_hyundai],
                         'Manufacturer_Isuzu': [manufacturer_isuzu],
                         'Manufacturer_Jaguar': [manufacturer_jaguar],
                         'Manufacturer_Jeep': [manufacturer_jeep],
                         'Manufacturer_Lamborghini': [manufacturer_lamborghini],
                         'Manufacturer_Land': [manufacturer_land],
                         'Manufacturer_Mahindra': [manufacturer_mahindra],
                         'Manufacturer_Maruti': [manufacturer_maruti],
                         'Manufacturer_Mercedes-Benz': [manufacturer_mercedes],
                         'Manufacturer_Mini': [manufacturer_mini],
                         'Manufacturer_Mitsubishi': [manufacturer_mitsubishi],
                         'Manufacturer_Nissan': [manufacturer_nissan],
                         'Manufacturer_Porsche': [manufacturer_porsche],
                         'Manufacturer_Renault': [manufacturer_renault],
                         'Manufacturer_Skoda': [manufacturer_skoda],
                         'Manufacturer_Smart': [manufacturer_smart],
                         'Manufacturer_Tata': [manufacturer_tata],
                         'Manufacturer_Toyota': [manufacturer_toyota],
                         'Manufacturer_Volkswagen': [manufacturer_volkswagen],
                         'Manufacturer_Volvo': [manufacturer_volvo],
                        })
    

    #get prediction from he ML model
    prediction = model.predict(data)
    prediction = round(prediction[0],2)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO car_details (manufacturer, k_driven, mileage, engine, power, seats, age, fuel_type, transmission, owner_type, email, prediction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (manufacturer, k_driven, mileage, engine, power, seats, age, fuel_type, transmission, owner_type, email, prediction)
    cursor.execute(sql, values)
    mysql.connection.commit()
    return render_template('output.html',username=username, manufacturer=manufacturer,k_driven=k_driven,mileage=mileage,engine=engine,power=power,seats=seats,age=age,fuel_type=fuel_type,transmission=transmission,owner_type=owner_type,prediction=prediction)
    



@app.route('/history')
def history():
    email = session.get('email')
    username = session.get('username')
    prompt=''
    if 'email' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM car_details WHERE email = %s',(email,))
        rows = cursor.fetchall()
        if rows == ():
            prompt="Sorry! You haven't utilised our service yet, so there's nothing to show you."
            return render_template('history.html', prompt = prompt, email = email, username = username)
        else:
            # retrieve the values
            rows = list(rows)
            manufacturer = rows[0]['manufacturer']
            k_driven = rows[0]['k_driven']
            mileage = rows[0]['mileage']
            engine = rows[0]['engine']
            power = rows[0]['power']
            seats = rows[0]['seats']
            age = rows[0]['age']
            fuel_type = rows[0]['fuel_type']
            transmission = rows[0]['transmission']
            owner_type = rows[0]['owner_type']
            email = rows[0]['email']
            prediction = rows[0]['prediction']
            return render_template('history.html',rows=rows, manufacturer=manufacturer,k_driven=k_driven,mileage=mileage,engine=engine,power=power,seats=seats,age=age,fuel_type=fuel_type,transmission=transmission,owner_type=owner_type,email=email,prediction=prediction,username = username)
    else:
        prompt='Please Sign In!'
        return render_template('login.html',prompt=prompt)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reach_us')
def contact():
    return render_template('contact.html')



if __name__=="__main__":
    app.run(debug=True) 


