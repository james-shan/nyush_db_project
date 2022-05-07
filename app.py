
from decimal import*
from flask import Flask, render_template, flash, request, session, url_for, redirect
from datetime import datetime,date
import pymysql.cursors
from dateutil.relativedelta import relativedelta
from math import ceil

#Create a Flask Instance
app = Flask(__name__)
#Add Databse
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'

#Initialize The Database
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='JM_Booking',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Secrete Key
app.config['SECRET_KEY'] = "ykcisstupid"
        
#Create a Form Class
#class NamerForm(FlaskForm):
#    name = StringField("What's your name", validators=[DataRequired()])
#    submit = SubmitField("Submit")
'''----------------------------------------------------------------------------------------------------'''

@app.route('/', methods=['GET'])
def index():
    flash("Welcome to the Online Booking System!")
    return render_template("index.html")
    

@app.route('/', methods=['POST'])
def public_info_search():
    error = None
    # fetch info from form
    departure_airport = request.form.get('departure_airport')
    arrival_airport = request.form.get('arrival_airport')
    departure_date = request.form.get('departure_date')
    return_date = request.form.get('return_date')
    departure_city = request.form.get('departure_city')
    arrival_city = request.form.get('arrival_city')
    airline_name = request.form.get('airline_name')
    flight_num = request.form.get('flight_num')
    arrival_date = request.form.get('arrival_date')
    

    # check for search type
    if departure_airport:
        if not departure_date:
            if return_date:
                error = 'Please enter departure date before return date'
                return render_template('index.html', error1 = error)
            # fetch search result
            query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                    FROM flight \
                    WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" '''.format(departure_airport,arrival_airport)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
        # case handling
            if not result:
                error = 'No outgoing flight exists'
                return render_template('index.html', error1=error)
        if departure_date:
            query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                FROM flight \
                WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" AND DATE(departure_time) = '{}' '''.format(departure_airport,arrival_airport,departure_date)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            if not result:
                error = 'No outgoing flight exists'
                return render_template('index.html', error1=error)
            if return_date:
                query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                    FROM flight \
                    WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" AND DATE(departure_time) = '{}' '''.format(arrival_airport, departure_airport,return_date)
                cursor = conn.cursor()
                cursor.execute(query)
                return_flight = cursor.fetchall()
                return render_template('index.html', search1=result, search2=return_flight)
        return render_template('index.html', search1=result)

    elif departure_city:
        if not departure_date:
            if return_date:
                error = 'Please enter departure date before return date'
                return render_template('index.html', error2 = error)
            
            query = '''SELECT DISTINCT airline_name,flight_num ,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                            WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            '''.format (departure_city, arrival_city)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            if not result:
                error = 'No outgoing flight exists'
                return render_template('index.html', error2=error)
        if departure_date:
            query = '''SELECT DISTINCT airline_name,flight_num ,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                        WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                        AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                        AND DATE(departure_time) = '{}' '''.format (departure_city, arrival_city, departure_date)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            if not result:
                error = 'No outgoing flight exists'
                return render_template('index.html', error2=error)
            if return_date:
                query = '''SELECT DISTINCT airline_name,flight_num,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                            WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND DATE(departure_time) = '{}' '''.format (arrival_city, departure_city, return_date)
                cursor = conn.cursor()
                cursor.execute(query)    
                return_flight = cursor.fetchall()
                return render_template('index.html', search1=result,search2=return_flight)
        return render_template('index.html', search1=result)
        
    elif airline_name:
        if departure_date:
            query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                    FROM flight \
                    WHERE status = 'Upcoming' AND airline_name = "{}" AND flight_num = {} AND DATE(departure_time) = '{}' '''.format(airline_name, int(flight_num), departure_date)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            if not result:
                error = 'No such flight exists'
                return render_template('index.html', error3=error)
            return render_template('index.html', search3=result)
        
        elif arrival_date:
            query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                    FROM flight \
                    WHERE status = 'Upcoming' AND airline_name = "{}" AND flight_num = {} AND DATE(arrival_time) = '{}' '''.format(airline_name, int(flight_num), arrival_date)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            if not result:
                error = 'No such flight exists'
                return render_template('index.html', error3=error)
            return render_template('index.html', search3=result)
        
        else:
            query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                    FROM flight \
                    WHERE status = 'Upcoming' AND airline_name = "{}" AND flight_num = {} '''.format(airline_name, int(flight_num))
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            if not result:
                error = 'No such flight exists'
                return render_template('index.html', error3=error)
            return render_template('index.html', search3=result)

         
        
'''----------------------------------------------------------------------------------------------------'''

    
#create custom Error Pages


'''----------------------------------------------------------------------------------------------------'''

#Create Register Form
'''
class RegisterForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password1 = StringField("Please set your passwords:", validators=[DataRequired()])
#    password2 = StringField("Please check your password again:", validators=[DataRequired()])
    submit = SubmitField("Submit")
'''

#Create Register Page
@app.route('/Register', methods=['GET', 'POST'])
def Register():
    return render_template("Register.html")

'''----------------------------------------------------------------------------------------------------'''

#Create Customer Register Page
@app.route('/Register/Customer', methods=['Get', 'POST'])
def Register_customer():
    if request.method == "POST":
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        name = request.form.get('Name')
        buildingNumber = request.form.get('buildingnumber')
        street = request.form.get('Street')
        city = request.form.get('City')
        state = request.form.get('State')
        phoneNumber = request.form.get('Phone Number')
        passportNumber = request.form.get('Passport Number')
        passportExpiration = request.form.get('Passport Expiration')
        passportCountry = request.form.get('Passport Country')
        dob = request.form.get('Date of Birth')

        #Check if the passwords entered twice are the same
        if password1 != password2:
            error = "Please enter the same passwords!"
            return render_template('Register_customer.html', error = error)

        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = '''SELECT * FROM customer WHERE email = '{}' '''.format(email)
        cursor.execute(query)
        #stores the results in a variable
        data = cursor.fetchone()

        #Exaute insertion or Raise error
        error = None
        if(data):
            #If the previous query returns data, then user exists
            error = "This user already exists"
            return render_template('Register_customer.html', error = error)

        else:
            sql = '''INSERT INTO customer VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(email, name,
                                                                                                            password1, buildingNumber,
                                                                                                            street, city, state,
                                                                                                            phoneNumber,
                                                                                                            passportNumber,
                                                                                                            passportExpiration,
                                                                                                            passportCountry, dob)

            cursor.execute(sql)
            conn.commit()
            cursor.close()
            session['customer'] = email
            return redirect(url_for('Customer_home'))

    return render_template("Register_customer.html")

'''----------------------------------------------------------------------------------------------------''' 

#Create Booking Agent Register Page
@app.route('/Register/Agent', methods=['Get', 'POST'])
def Register_agent():
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get('password2')   
        agent_id = request.form.get('Agent_id')

        #Check if the passwords entered twice are the same
        if password1 != password2:
            error = "Please enter the same passwords!"
            return render_template('Register_agent.html', error = error)

        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = '''SELECT * FROM booking_agent WHERE email = '{}' '''.format(email)
        cursor.execute(query)
        #stores the results in a variable
        data = cursor.fetchone()

        #Exaute insertion or Raise error
        error = None
        if(data):
            #If the previous query returns data, then user exists
            error = "This user already exists"
            return render_template('Register_agent.html', error = error)

        else:
            query = '''INSERT INTO booking_agent VALUES ('{}', '{}', '{}')'''.format(email, password1, agent_id)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            session['agent'] = email
            return redirect(url_for('Agent_home'))

    return render_template("Register_agent.html")
'''        except:
            error = "Register failed"
            return render_template('Register.html', error = error)'''

'''----------------------------------------------------------------------------------------------------'''

#Create Airline Staff Register Page
@app.route('/Register/Staff', methods=['Get', 'POST'])
def Register_staff():
    if request.method == "POST":
        username = request.form.get('Username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')   
        first_name = request.form.get('First_name')
        last_name = request.form.get('Last_name')
        dob = request.form.get('Date of Birth')
        airline_name = request.form.get('Airline_name')

        #Check if the passwords entered twice are the same
        if password1 != password2:
            error = "Please enter the same passwords!"
            return render_template('Register_customer.html', error = error)

        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = '''SELECT * FROM airline_staff WHERE username = '{}' '''.format(username)
        cursor.execute(query)
        #stores the results in a variable
        data = cursor.fetchone()

        #Exaute insertion or Raise error
        error = None
        if(data):
            #If the previous query returns data, then user exists
            error = "This user already exists"
            return render_template('Register_staff.html', error = error)

        else:
            query = '''INSERT INTO airline_staff VALUES ('{}', '{}', '{}', '{}', '{}', '{}')'''.format(username, password1, first_name, last_name, dob, airline_name)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            session['staff'] = username
            return redirect(url_for('Staff_home'))

    return render_template("Register_staff.html")

'''----------------------------------------------------------------------------------------------------'''    

#Create Login Page
@app.route('/Login', methods=['GET', 'POST'])
def Login():
    return render_template("Login.html")

'''----------------------------------------------------------------------------------------------------'''

#Create Customer Login Page
@app.route('/Login/Customer', methods=['GET','POST'])
def Login_customer():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = conn.cursor()
        query = ''' SELECT password FROM customer WHERE email = '{}' and password = '{}' '''.format(email, password)
        cursor.execute(query)
        #Store the result in a variable     
        data = cursor.fetchone()

        #Login or Raise error
        if (data):
            session['customer'] = email
            username = email
            return redirect(url_for('Customer_home'))
            #return render_template('Customer_home.html',username = username, status = 'customer')
        else:
            error = 'Incorrect Email or Password'
            return render_template('Login_customer.html', error = error)

    return render_template('Login_customer.html')

'''----------------------------------------------------------------------------------------------------'''        

#Create Agent Login Page
@app.route('/Login/Agent', methods=['GET','POST'])
def Login_agent():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = conn.cursor()
        query = ''' SELECT * FROM booking_agent WHERE email = '{}' and password = '{}' '''.format(email, password)
        cursor.execute(query)
        #Store the result in a variable          
        data = cursor.fetchone()

        #Login or Raise error
        if (data):
            session['agent'] = email
            return redirect(url_for('Agent_home'))
        else:
            error = '''Incorrect Email or Password'''
            return render_template('Login_agent.html', error = error)

    return render_template('Login_agent.html')

'''----------------------------------------------------------------------------------------------------'''

#Create Staff Login Page
@app.route('/Login/Staff', methods=['GET','POST'])
def Login_staff():
    if request.method == "POST":
        username = request.form.get('Username')
        password = request.form.get('password')

        cursor = conn.cursor()
        query = ''' SELECT password FROM airline_staff WHERE username = '{}' and password = '{}' '''.format(username, password)
        cursor.execute(query)
        #Store the result in a variable          
        data = cursor.fetchone()

        #Login or Raise error
        if (data):
            session['staff'] = username
            return redirect(url_for('Staff_home'))
        else:
            error = 'Incorrect Username or Password'
            return render_template('Login_staff.html', error = error)

    return render_template('Login_staff.html')

'''----------------------------------------------------------------------------------------------------'''

#Customer Home page
@app.route('/Customer', methods=['GET', 'POST'])
def Customer_home():
    if 'customer' in session:
        #main home page attributes
        username = session['customer']
        departure_airport = request.form.get('departure_airport')
        arrival_airport = request.form.get('arrival_airport')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        departure_city = request.form.get('departure_city')
        arrival_city = request.form.get('arrival_city')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        '''---------------------------------------------'''
        #purchase ticket attributes
        purchase_flight_number = request.form.get('purchase_flight_num')
        purchase_airline_name = request.form.get('purchase_airline_name')        
        '''---------------------------------------------'''

        query = '''SELECT DISTINCT F.airline_name, F.flight_num, F.departure_time , F.arrival_time, F.departure_airport, F.arrival_airport, F.status, \
                    COUNT(F.flight_num) AS ticket_num \
                    FROM flight as F, ticket as T, purchases as P \
                    WHERE F.flight_num = T.flight_num AND T.ticket_id = P.ticket_id AND P.customer_email = '{}' \
                    GROUP BY F.airline_name,F.flight_num'''.format(username)
        cursor = conn.cursor()
        cursor.execute(query)    
        view_my_flight_result = cursor.fetchall()

        if 'sold_out_message' in session:
            session.pop('sold_out_message')
            return render_template('Customer_home.html', username = username, status = 'customer', sold_out_message = True, default_customer_view = view_my_flight_result)
        
        if 'buy_limit_message' in session:
            session.pop('buy_limit_message')
            return render_template('Customer_home.html', username = username, status = 'customer', buy_limit_message= True, default_customer_view = view_my_flight_result)

        if purchase_flight_number and purchase_airline_name:
            session['purchase_flight_number'] = purchase_flight_number
            session['purchase_airline_name'] = purchase_airline_name
            return redirect(url_for('Customer_purchase_ticket'))
            #return Customer_purchase_ticket(purchase_flight_num,purchase_airline_name,username)
        #if ccn and success_price:
            #return Customer_purchase_success(username,success_airline_name,success_flight_num, ccn,success_price,success_ticket_num)

        if not departure_airport and not departure_city:
            if (start_date):
                query = '''SELECT DISTINCT F.airline_name, F.flight_num, F.departure_time , F.arrival_time, F.departure_airport, F.arrival_airport, F.status, \
                    COUNT(F.flight_num) AS ticket_num \
                    FROM flight as F, ticket as T, purchases as P \
                    WHERE F.flight_num = T.flight_num AND T.ticket_id = P.ticket_id AND P.customer_email = '{}' \
                        AND (DATE(F.departure_time) BETWEEN "{}" AND "{}") \
                    GROUP BY F.airline_name,F.flight_num'''.format(username, start_date, end_date)
                cursor = conn.cursor()
                cursor.execute(query)
                view_my_flight_result = cursor.fetchall()
            return render_template('Customer_home.html', username = username, status = 'customer', default_customer_view = view_my_flight_result)

        elif departure_airport:
            # fetch search result
            if not departure_date:
                if return_date:
                    error = "Please enter departure date before return date"
                    return render_template('Customer_home.html', username = username, status = 'customer', cus_error1=error)
                query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                        FROM flight \
                        WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" '''.format(departure_airport,arrival_airport)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                if not result:
                    error = 'No outgoing flight exists'
                    return render_template('Customer_home.html', username = username, status = 'customer', cus_error1=error)
            if departure_date:
                query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                    FROM flight \
                    WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" AND DATE(departure_time) = '{}' '''.format(departure_airport,arrival_airport,departure_date)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                if not result:
                    error = 'No outgoing flight exists'
                    return render_template('Customer_home.html', username = username, status = 'customer', cus_error1=error)
                if return_date:
                    query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                        FROM flight \
                        WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" AND DATE(departure_time) = '{}' '''.format(arrival_airport, departure_airport,return_date)
                    cursor = conn.cursor()
                    cursor.execute(query)
                    return_flight = cursor.fetchall()
                    return render_template('Customer_home.html', username = username, status = 'customer', cus_search1=result, cus_search2=return_flight)
            return render_template('Customer_home.html', username = username, status = 'customer', cus_search1=result)

        if departure_city:
            if not departure_date:
                if return_date:
                    error = "Please enter departure date before return date"
                    return render_template('Customer_home.html', username = username, status = 'customer', cus_error2=error)
                
                query = '''SELECT DISTINCT airline_name,flight_num ,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                            WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            '''.format (departure_city, arrival_city)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                if not result:
                    error = 'No outgoing flight exists'
                    return render_template('Customer_home.html', username = username, status = 'customer',cus_error2=error)
            if departure_date:
                query = '''SELECT DISTINCT airline_name,flight_num ,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                            WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND DATE(departure_time) = '{}' '''.format (departure_city, arrival_city, departure_date)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                if not result:
                    error = 'No outgoing flight exists'
                    return render_template('Customer_home.html', username = username, status = 'customer',cus_error2=error)
                if return_date:
                    query = '''SELECT DISTINCT airline_name,flight_num,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                                WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                                AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                                AND DATE(departure_time) = '{}' '''.format (arrival_city, departure_city, return_date)
                    
                    cursor = conn.cursor()
                    cursor.execute(query)    
                    return_flight = cursor.fetchall()
                    return render_template('Customer_home.html', username = username, status = 'customer', cus_search1=result, cus_search2=return_flight)
            
            return render_template('Customer_home.html', username = username, status = 'customer', cus_search1=result)

    else:
        return redirect(url_for('index')) 

'''----------------------------------------------------------------------------------------------------'''
@app.route('/Customer/Purchase_ticket', methods=['GET','POST'])
def Customer_purchase_ticket():
    #get data from customer home
    if 'customer' in session and 'purchase_airline_name' in session and 'purchase_flight_number' in session: 
        username = session['customer']
        purchase_airline_name = session['purchase_airline_name']
        purchase_flight_number = session['purchase_flight_number']
        
        #get data from input
        ccn = request.form.get('ccn')
        success_price = request.form.get('success_price')
        success_airline_name = request.form.get('success_airline_name')
        success_flight_num = request.form.get('success_flight_num')
        success_ticket_num = request.form.get('ticket_num')
        #Get into purchase success page
        if ccn and success_price and success_airline_name and success_flight_num and success_ticket_num:
            session['ccn']=ccn
            session['success_price']=success_price
            session['success_airline_name']=success_airline_name
            session['success_flight_num']=success_flight_num
            session['success_ticket_num']=success_ticket_num
            return redirect(url_for('Customer_purchase_success'))
        #judge for entering purchase
        condition_query = '''SELECT COUNT(flight_num) AS ticket_bought FROM ticket NATURAL JOIN purchases \
                            WHERE customer_email = '{}' AND flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num,airline_name'''.format(username,purchase_flight_number,purchase_airline_name)
        cursor = conn.cursor()
        cursor.execute(condition_query)    
        condition_result = cursor.fetchone()
        if condition_result is None:
            condition_num = 0
        elif condition_result.get('ticket_bought') < 5:
            condition_num = 0
        else:
            condition_num = 1

        if condition_num == 0:
            condition_query = '''SELECT COUNT(airline_name) FROM ticket WHERE airline_name = '{}' AND flight_num = {} GROUP BY \
                                airline_name,flight_num '''.format(purchase_airline_name,purchase_flight_number)
            cursor = conn.cursor()
            cursor.execute(condition_query)    
            condition_result = cursor.fetchone()
            if condition_result is None:
                query = '''SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, price, seats AS seats_remaining \
                            FROM airplane NATURAL JOIN flight \
                            WHERE flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num '''.format(purchase_flight_number,purchase_airline_name)
            else:
                query = '''SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, price, seats - COUNT(ticket_id) AS seats_remaining \
                            FROM airplane NATURAL JOIN flight NATURAL JOIN ticket \
                            WHERE flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num \
                            HAVING seats_remaining > 0 '''.format(purchase_flight_number,purchase_airline_name)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchone()
            #print(result)
            if result:
                #display limit message
                if 'purchase_limit_message' in session:
                    session.pop('purchase_limit_message')
                    return render_template('Customer_purchase_ticket.html', status = 'customer',flight_confirm = result, purchase_limit_message = True)
                return render_template('Customer_purchase_ticket.html', status = 'customer',flight_confirm = result)
            else:
                session['sold_out_message'] = True
       
                session.pop('purchase_airline_name')
                session.pop('purchase_flight_number')
                return redirect(url_for('Customer_home'))
                
        else:
            session['buy_limit_message'] = True
            session.pop('purchase_airline_name')
            session.pop('purchase_flight_number')
            return redirect(url_for('Customer_home'))
    else:
        return redirect(url_for('index')) 

'''----------------------------------------------------------------------------------------------------'''
@app.route('/Customer/Purchase_success', methods=['GET','POST'])
def Customer_purchase_success():
    if 'customer' in session and 'ccn' in session:
        username=session['customer']
        ccn=session['ccn']
        price=session['success_price']
        airline_name=session['success_airline_name']
        flight_num=session['success_flight_num']
        ticket_num=session['success_ticket_num']

        session.pop('ccn')
        session.pop('success_price')
        session.pop('success_airline_name')
        session.pop('success_flight_num')
        session.pop('success_ticket_num')

        condition_query = '''SELECT COUNT(flight_num) AS ticket_bought FROM ticket NATURAL JOIN purchases \
                            WHERE customer_email = '{}' AND flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num,airline_name'''.format(username,flight_num,airline_name)
        cursor = conn.cursor()
        cursor.execute(condition_query)    
        condition_result = cursor.fetchone()
        
        if condition_result is None:
            condition_num = 0
        elif condition_result.get('ticket_bought') + int(ticket_num) <= 5:
            condition_num = 0
        else:
            condition_num = 1
        if condition_num == 0:
            ticket_num_list = []
            for i in range(int(ticket_num)):
                purchase_date = date.today()
                query = '''SELECT MAX(ticket_id)+1 AS new_ticket_id FROM ticket'''
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchone()
                ticket_id = result.get('new_ticket_id')
                ticket_num_list.append(ticket_id)
                query1 = ''' INSERT INTO ticket (ticket_id, airline_name,flight_num) VALUES\
                            ('{}','{}',{}); '''.format(ticket_id,airline_name,flight_num)
                query2 = '''INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date, credit_card_number, figure) VALUES \
                            ('{}','{}',NULL,'{}','{}','{}') '''.format(ticket_id,username,purchase_date,ccn,price)
                cursor = conn.cursor()
                cursor.execute(query1)
                cursor.execute(query2)
                conn.commit()
                cursor.close()
            if len(ticket_num_list) == 1:
                query = '''SELECT * FROM purchases WHERE ticket_id = {}'''.format(ticket_num_list[0])
            else:
                ticket_numbers = tuple(ticket_num_list)
                query = '''SELECT * FROM purchases WHERE ticket_id IN {}'''.format(ticket_numbers)
            cursor = conn.cursor()
            #print(query)
            cursor.execute(query)    
            result = cursor.fetchall()
            success_message = '''Purchase Success! Automatically back home in 3 seconds...'''.format(airline_name, flight_num)
            session.pop('purchase_airline_name')
            session.pop('purchase_flight_number')
            return render_template('Customer_purchase_success.html',username=username, status = "customer", success_message = success_message,result = result) 
        else:
            session['purchase_limit_message'] = True
            return redirect(url_for('Customer_purchase_ticket'))
'''----------------------------------------------------------------------------------------------------'''
   
@app.route('/Customer/Track_my_spending', methods=['GET', 'POST'])
def Customer_Track_my_spending():
    end_date = date.today()
    last_year = end_date + relativedelta(months=-12)
    total_price = 0
    default = 6
    labels = []
    values = [] 

    cursor = conn.cursor()
    query = '''SELECT sum(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email = '{}' AND purchase_date >= '{}' '''.format(session['customer'], last_year)
    cursor.execute(query)
    data = cursor.fetchone()
    last_year_spending = data['sum(price)']

    start_date = request.form.get('Start_date')
    if (start_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = request.form.get('End_date')
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        if (int(end_date.year)-int(start_date.year)) == 0:
            diff = (int(end_date.month)-int(start_date.month))
        else:
            diff = (int(end_date.year)-int(start_date.year)-1)*12 + (12-int(start_date.month)+int(end_date.month))
        default = diff+1
        #print(default)

    for i in range(default):
        month = (end_date + relativedelta(months=-(default-i-1))).month
        year = (end_date + relativedelta(months=-(default-i-1))).year
        labels.append(str(year)+'-'+str(month))
        #print(labels)
        query = '''SELECT sum(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email = '{}' AND MONTH(purchase_date) = '{}' And YEAR(purchase_date) = '{}' '''.format(session['customer'], month, year)
        cursor.execute(query)
        data = cursor.fetchone()
        #print(data)
        if data['sum(price)'] is None:
            values.append(0)
        else:
            values.append(int(data['sum(price)']))
        #print(values)
    conn.commit()
    cursor.close()

    return render_template('Customer_Track_my_spending.html', status = 'customer', last_year_spending =last_year_spending, labels = labels, values = values)

'''----------------------------------------------------------------------------------------------------'''

#Agent Home page
@app.route('/Agent', methods=['GET', 'POST'])
def Agent_home():
    if 'agent' in session:
        #main home page attributes
        username = session['agent']
        departure_airport = request.form.get('departure_airport')
        arrival_airport = request.form.get('arrival_airport')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        departure_city = request.form.get('departure_city')
        arrival_city = request.form.get('arrival_city')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        '''---------------------------------------------'''
        #purchase ticket attributes
        purchase_flight_number = request.form.get('purchase_flight_num')
        purchase_airline_name = request.form.get('purchase_airline_name')        
        '''---------------------------------------------'''

        query = '''SELECT DISTINCT F.airline_name, F.flight_num, F.departure_time , F.arrival_time, F.departure_airport, F.arrival_airport, F.status, \
                    P.customer_email AS customer_email\
                    FROM flight as F, ticket as T, purchases as P,booking_agent as B \
                    WHERE F.flight_num = T.flight_num AND T.ticket_id = P.ticket_id AND B.booking_agent_id = P.booking_agent_id AND B.email = '{}' \
                    GROUP BY F.airline_name,F.flight_num'''.format(username)
        cursor = conn.cursor()
        cursor.execute(query)    
        view_my_flight_result = cursor.fetchall()

        if 'sold_out_message' in session:
            session.pop('sold_out_message')
            return render_template('Agent_home.html', username = username, status = 'agent', sold_out_message = True, default_agent_view = view_my_flight_result)
        
        if 'buy_limit_message' in session:
            session.pop('buy_limit_message')
            return render_template('Agent_home.html', username = username, status = 'agent', buy_limit_message= True, default_agent_view = view_my_flight_result)
        
        if 'no_permit_message' in session:
            session.pop('no_permit_message')
            return render_template('Agent_home.html', username = username, status = 'agent', no_permit_message= True, default_agent_view = view_my_flight_result, airline_name = purchase_airline_name)


        if purchase_flight_number and purchase_airline_name:
            session['purchase_flight_number'] = purchase_flight_number
            session['purchase_airline_name'] = purchase_airline_name
            return redirect(url_for('Agent_purchase_ticket'))
            #return Customer_purchase_ticket(purchase_flight_num,purchase_airline_name,username)
        #if ccn and success_price:
            #return Customer_purchase_success(username,success_airline_name,success_flight_num, ccn,success_price,success_ticket_num)

        if not departure_airport and not departure_city:
            if (start_date):
                query = '''SELECT DISTINCT F.airline_name, F.flight_num, F.departure_time , F.arrival_time, F.departure_airport, F.arrival_airport, F.status, \
                    P.customer_email as customer_email \
                    FROM flight as F, ticket as T, purchases as P, booking_agent as B \
                    WHERE F.flight_num = T.flight_num AND T.ticket_id = P.ticket_id AND B.booking_agent_id = P.booking_agent_id AND B.email = '{}' \
                        AND (DATE(F.departure_time) BETWEEN "{}" AND "{}") \
                    GROUP BY F.airline_name,F.flight_num'''.format(username, start_date, end_date)
                cursor = conn.cursor()
                cursor.execute(query)
                view_my_flight_result = cursor.fetchall()
            return render_template('Agent_home.html', username = username, status = 'agent', default_agent_view = view_my_flight_result)

        elif departure_airport:
            # fetch search result
            if not departure_date:
                if return_date:
                    error = "Please enter departure date before return date"
                    return render_template('Agent_home.html', username = username, status = 'agent', agent_error1=error)
                query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                        FROM flight \
                        WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" '''.format(departure_airport,arrival_airport)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                if not result:
                    error = 'No outgoing flight exists'
                    return render_template('Agent_home.html', username = username, status = 'agent', agent_error1=error)
            if departure_date:
                query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                    FROM flight \
                    WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" AND DATE(departure_time) = '{}' '''.format(departure_airport,arrival_airport,departure_date)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                if not result:
                    error = 'No outgoing flight exists'
                    return render_template('Agent_home.html', username = username, status = 'agent', agent_error1=error)
                if return_date:
                    query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                        FROM flight \
                        WHERE status = 'Upcoming' AND departure_airport = "{}" AND arrival_airport = "{}" AND DATE(departure_time) = '{}' '''.format(arrival_airport, departure_airport,return_date)
                    cursor = conn.cursor()
                    cursor.execute(query)
                    return_flight = cursor.fetchall()
                    return render_template('Agent_home.html', username = username, status = 'agent', agent_search1=result, agent_search2=return_flight)
            return render_template('Agent_home.html', username = username, status = 'agent', agent_search1=result)

        if departure_city:
            if not departure_date:
                if return_date:
                    error = "Please enter departure date before return date"
                    return render_template('Agent_home.html', username = username, agent = 'agent', agent_error2=error)
                
                query = '''SELECT DISTINCT airline_name,flight_num ,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                            WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            '''.format (departure_city, arrival_city)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                if not result:
                    error = 'No outgoing flight exists'
                    return render_template('Agent_home.html', username = username, status = 'agent',agent_error2=error)
            if departure_date:
                query = '''SELECT DISTINCT airline_name,flight_num ,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                            WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                            AND DATE(departure_time) = '{}' '''.format (departure_city, arrival_city, departure_date)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                if not result:
                    error = 'No outgoing flight exists'
                    return render_template('Agent_home.html', username = username, status = 'agent', agent_error2=error)
                if return_date:
                    query = '''SELECT DISTINCT airline_name,flight_num,departure_time, arrival_time, departure_airport, arrival_airport, status  FROM flight \
                                WHERE status = 'Upcoming' AND departure_airport IN(SELECT airport_name FROM airport WHERE airport_city = "{}") \
                                AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = "{}") \
                                AND DATE(departure_time) = '{}' '''.format (arrival_city, departure_city, return_date)
                    
                    cursor = conn.cursor()
                    cursor.execute(query)    
                    return_flight = cursor.fetchall()
                    return render_template('Agent_home.html', username = username, status = 'agent', agent_search1=result, agent_search2=return_flight)
            
            return render_template('Agent_home.html', username = username, status = 'agent', agent_search1=result)

    else:
        return redirect(url_for('index'))  
'''----------------------------------------------------------------------------------------------------'''
@app.route('/Agent/Purchase_ticket', methods=['GET','POST'])
def Agent_purchase_ticket():
    #get data from customer home
    if 'agent' in session and 'purchase_airline_name' in session and 'purchase_flight_number' in session: 
        username = session['agent']
        purchase_airline_name = session['purchase_airline_name']
        purchase_flight_number = session['purchase_flight_number']
        #get data from input
        ccn = request.form.get('ccn')
        success_price = request.form.get('success_price')
        success_airline_name = request.form.get('success_airline_name')
        success_flight_num = request.form.get('success_flight_num')
        success_ticket_num = request.form.get('ticket_num')
        cus_email = request.form.get('cus_email')
        #Get into purchase success page
        if ccn and success_price and success_airline_name and success_flight_num and success_ticket_num and cus_email:
            session['ccn']=ccn
            session['success_price']=success_price
            session['success_airline_name']=success_airline_name
            session['success_flight_num']=success_flight_num
            session['success_ticket_num']=success_ticket_num
            session['cus_email']=cus_email
            return redirect(url_for('Agent_purchase_success'))
        #judge for agent permission
        permit_query = '''SELECT airline_name from booking_agent_work_for WHERE email = '{}' '''.format(username)
        cursor = conn.cursor()
        cursor.execute(permit_query)    
        permit_result = cursor.fetchall()
        permitted_airline_name_list=[]
        for line in permit_result:
            permitted_airline_name_list.append(line['airline_name'])
        if purchase_airline_name not in permitted_airline_name_list:
            session['no_permit_message'] = True
            session.pop('purchase_airline_name')
            session.pop('purchase_flight_number')
            return redirect(url_for('Agent_home'))

        #judge for remaining tickets
        condition_query = '''SELECT COUNT(flight_num) AS ticket_bought FROM ticket NATURAL JOIN purchases NATURAL JOIN booking_agent \
                            WHERE email = '{}' AND flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num,airline_name'''.format(username,purchase_flight_number,purchase_airline_name)
        cursor = conn.cursor()
        cursor.execute(condition_query)    
        condition_result = cursor.fetchone()
        if condition_result is None:
            condition_num = 0
        elif condition_result.get('ticket_bought') < 30:
            condition_num = 0
        else:
            condition_num = 1

        if condition_num == 0:
            condition_query = '''SELECT COUNT(airline_name) FROM ticket WHERE airline_name = '{}' AND flight_num = {} GROUP BY \
                                airline_name,flight_num '''.format(purchase_airline_name,purchase_flight_number)
            cursor = conn.cursor()
            cursor.execute(condition_query)    
            condition_result = cursor.fetchone()
            if condition_result is None:
                query = '''SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, price, seats AS seats_remaining \
                            FROM airplane NATURAL JOIN flight \
                            WHERE flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num '''.format(purchase_flight_number,purchase_airline_name)
            else:
                query = '''SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, price, seats - COUNT(ticket_id) AS seats_remaining \
                            FROM airplane NATURAL JOIN flight NATURAL JOIN ticket \
                            WHERE flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num \
                            HAVING seats_remaining > 0 '''.format(purchase_flight_number,purchase_airline_name)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchone()
            #print(result)
            if result:
                #display limit message
                if 'purchase_limit_message' in session:
                    session.pop('purchase_limit_message')
                    return render_template('Agent_purchase_ticket.html', status = 'agent',flight_confirm = result, purchase_limit_message = True)
                return render_template('Agent_purchase_ticket.html', status = 'agent',flight_confirm = result)
            else:
                session['sold_out_message'] = True
       
                session.pop('purchase_airline_name')
                session.pop('purchase_flight_number')
                return redirect(url_for('Agent_home'))
                
        else:
            session['buy_limit_message'] = True
            session.pop('purchase_airline_name')
            session.pop('purchase_flight_number')
            return redirect(url_for('Agent_home'))
    else:
        return redirect(url_for('index')) 

'''----------------------------------------------------------------------------------------------------'''

@app.route('/Agent/Purchase_success', methods=['GET','POST'])
def Agent_purchase_success():
    if 'agent' in session and 'ccn' in session:
        username=session['agent']
        ccn=session['ccn']
        price=session['success_price']
        airline_name=session['success_airline_name']
        flight_num=session['success_flight_num']
        ticket_num=session['success_ticket_num']
        cus_email=session['cus_email']

        session.pop('ccn')
        session.pop('success_price')
        session.pop('success_airline_name')
        session.pop('success_flight_num')
        session.pop('success_ticket_num')
        session.pop('cus_email')

        condition_query1= '''SELECT COUNT(flight_num) AS ticket_bought FROM ticket NATURAL JOIN purchases \
                            WHERE customer_email = '{}' AND flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num,airline_name'''.format(cus_email,flight_num,airline_name)
        cursor = conn.cursor()
        cursor.execute(condition_query1)    
        condition_result1 = cursor.fetchone()
        
        if condition_result1 is None:
            condition_num = 0
        elif condition_result1.get('ticket_bought') + int(ticket_num) <= 5:
            condition_num = 0
        else:
            condition_num = 1
        
        condition_query2= '''SELECT COUNT(flight_num) AS ticket_bought FROM ticket NATURAL JOIN purchases NATURAL JOIN booking_agent\
                            WHERE email = '{}' AND flight_num = {} AND airline_name = '{}' \
                            GROUP BY flight_num,airline_name'''.format(username,flight_num,airline_name)
        cursor = conn.cursor()
        cursor.execute(condition_query2)    
        condition_result2 = cursor.fetchone()
        if condition_result2 is None:
            pass
        elif condition_result2.get('ticket_bought') + int(ticket_num) <= 30:
            pass
        else:
            condition_num +=1
        
        if condition_num == 0:
            ticket_num_list = []
            for i in range(int(ticket_num)):
                purchase_date = date.today()
                query = '''SELECT MAX(ticket_id)+1 AS new_ticket_id FROM ticket'''
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchone()
                ticket_id = result.get('new_ticket_id')
                ticket_num_list.append(ticket_id)
                prepare_query = '''SELECT booking_agent_id FROM booking_agent WHERE email = '{}' '''.format(username)
                cursor = conn.cursor()
                cursor.execute(prepare_query)    
                result = cursor.fetchone()
                agent_id = result['booking_agent_id']
                query1 = ''' INSERT INTO ticket (ticket_id, airline_name,flight_num) VALUES\
                            ('{}','{}',{}); '''.format(ticket_id,airline_name,flight_num)
                query2 = '''INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date, credit_card_number, figure) VALUES \
                            ('{}','{}',{},'{}','{}','{}') '''.format(ticket_id,cus_email,agent_id, purchase_date,ccn,price)
                cursor = conn.cursor()
                cursor.execute(query1)
                cursor.execute(query2)
                conn.commit()
                cursor.close()
            if len(ticket_num_list) == 1:
                query = '''SELECT * FROM purchases WHERE ticket_id = {}'''.format(ticket_num_list[0])
            else:
                ticket_numbers = tuple(ticket_num_list)
                query = '''SELECT * FROM purchases WHERE ticket_id IN {}'''.format(ticket_numbers)
            cursor = conn.cursor()
            #print(query)
            cursor.execute(query)    
            result = cursor.fetchall()
            success_message = '''Purchase Success! Automatically back home in 3 seconds...'''.format(airline_name, flight_num)
            session.pop('purchase_airline_name')
            session.pop('purchase_flight_number')
            return render_template('Agent_purchase_success.html',username=username, status = "agent", success_message = success_message,result = result) 
        else:
            session['purchase_limit_message'] = True
            return redirect(url_for('Agent_purchase_ticket'))

'''----------------------------------------------------------------------------------------------------'''

@app.route('/Agent/View_my_commission', methods=['GET', 'POST'])
def View_my_commission():
    end_date = date.today()
    last_month = end_date + relativedelta(days=-30)

    #User Customized Range
    start_date = request.form.get('Start_date')
    if (start_date):
        end_date = request.form.get('End_date')
        cursor = conn.cursor()
        query = '''SELECT SUM(flight.price)*0.1, COUNT(ticket.ticket_id) FROM ticket NATURAL JOIN flight NATURAL JOIN purchases, booking_agent
                WHERE purchases.booking_agent_id = booking_agent.booking_agent_id 
                AND booking_agent.email='{}' 
                AND purchases.purchase_date >= '{}' AND purchases.purchase_date <= '{}' '''.format(session['agent'], start_date, end_date)
        cursor.execute(query)

    else:
        #SQL
        cursor = conn.cursor()
        query = '''SELECT SUM(flight.price)*0.1, COUNT(ticket.ticket_id) FROM ticket NATURAL JOIN flight NATURAL JOIN purchases, booking_agent
                WHERE purchases.booking_agent_id = booking_agent.booking_agent_id 
                AND booking_agent.email='{}' 
                AND purchases.purchase_date >= '{}' '''.format(session['agent'], last_month)
        cursor.execute(query)
    data = cursor.fetchone()

    if data['SUM(flight.price)*0.1'] is None:
        total_com = 0
    else:
        total_com = float(data['SUM(flight.price)*0.1']) 
    if data['COUNT(ticket.ticket_id)'] == 0:
        total_tickets = 0
        avg_com = 0
    else:
        total_tickets = float(data['COUNT(ticket.ticket_id)'])
        avg_com = format(total_com / total_tickets, '.2f')
#    print(data)
#    print(total_com, total_tickets, avg_com)
    conn.commit()
    cursor.close()

    return render_template('Agent_view_my_commission.html', status='agent', total_com = total_com, total_tickets=total_tickets , avg_com = avg_com)

'''----------------------------------------------------------------------------------------------------'''

@app.route('/Agent/View_top_customers', methods=['GET', 'POST'])
def View_top_customers():
    end_date = date.today()
    last_month = end_date + relativedelta(months=-6)
    last_year = end_date + relativedelta(months=-12)

    cursor = conn.cursor()
    #query Top five customer with number of tickets
    query ='''SELECT purchases.customer_email, COUNT(ticket.ticket_id) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, booking_agent
            WHERE booking_agent.booking_agent_id = purchases.booking_agent_id AND booking_agent.email = '{}' AND purchases.purchase_date >= '{}'
            GROUP BY purchases.customer_email'''.format(session['agent'], last_month)
    cursor.execute(query)
    data = cursor.fetchall()
    # Select Top 5
    data = sorted(data, key=lambda x: x["COUNT(ticket.ticket_id)"], reverse=True)
    chart1_labels = [row['customer_email'] for row in data]
    if len(chart1_labels) <= 5:
        for i in range(5-len(chart1_labels)):
            chart1_labels.append(0)
    else:
        chart1_labels = chart1_labels[:4]
    chart1_values = [row['COUNT(ticket.ticket_id)'] for row in data]
    if len(chart1_values) <= 5:
        for i in range(5-len(chart1_values)):
            chart1_values.append(0)
    else:
        chart1_values = chart1_values[:4]
    print(chart1_labels)
    print(chart1_values)

    #query Top five customer with commissions
    query ='''SELECT purchases.customer_email, SUM(flight.price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, booking_agent
            WHERE booking_agent.booking_agent_id = purchases.booking_agent_id AND booking_agent.email = '{}' AND purchases.purchase_date >= '{}'
            GROUP BY purchases.customer_email'''.format(session['agent'], last_year)
    cursor.execute(query)
    data = cursor.fetchall()
    # Select Top 5
    data = sorted(data, key=lambda x: x["SUM(flight.price)"], reverse=True)
    chart2_labels = [row['customer_email'] for row in data]
    if len(chart2_labels) <= 5:
        for i in range(5-len(chart2_labels)):
            chart2_labels.append(0)
    else:
        chart2_labels = chart2_labels[:4]
    chart2_values = [float(row['SUM(flight.price)'])*0.1 for row in data]
    if len(chart2_values) <= 5:
        for i in range(5-len(chart2_values)):
            chart2_values.append(0)
    else:
        chart2_values = chart2_values[:4]
    print(chart2_labels)
    print(chart2_values)  

    conn.commit()
    cursor.close()

    return render_template('Agent_view_top_customers.html', status='agent',
        chart1_labels = chart1_labels, chart1_values = chart1_values,
        chart2_labels = chart2_labels, chart2_values = chart2_values
    )    

'''----------------------------------------------------------------------------------------------------'''


'''----------------------------------------------------------------------------------------------------'''

#Staff Home page
@app.route('/Staff', methods=['GET', 'POST'])
def Staff_home():
    if 'staff' in session:
        username = session['staff']
        #Find staff Airline and Permission
        cursor = conn.cursor()
        query = '''SELECT airline_name FROM airline_staff WHERE username ='{}' '''.format(session['staff'])
        cursor.execute(query)
        data = cursor.fetchone()
        session['airline_name'] = data['airline_name']
        staff_airline_name = session['airline_name']
        query = '''SELECT permission_type FROM airline_staff NATURAL JOIN permission WHERE username = '{}' '''.format(session['staff'])
        cursor.execute(query)
        data = cursor.fetchall()    
        for row in data:
            if 'Admin' in row:
                session['Admin'] = True
            else:
                session['Admin'] = False
            if 'Operator' in row:
                session['Operator'] = True
            else:
                session['Operator'] = False
        conn.commit()
        cursor.close()
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        detail_airline_name = request.form.get('detail_airline_name')
        detail_flight_num = request.form.get('detail_flight_num')
        if not start_date and not end_date:
            start_date = date.today()
            end_date = start_date + relativedelta(days=+30)
        
        query = '''SELECT DISTINCT airline_name, flight_num, departure_time , arrival_time, departure_airport, arrival_airport, status \
                    FROM flight WHERE airline_name = '{}'  AND (DATE(departure_time) BETWEEN "{}" AND "{}")'''.format(staff_airline_name, start_date, end_date)
        #print(query)
        cursor = conn.cursor()
        cursor.execute(query)    
        view_result = cursor.fetchall()

        if detail_airline_name and detail_flight_num:
            session['detail_airline_name'] = detail_airline_name
            session['detail_flight_num'] = detail_flight_num
            return redirect(url_for('Staff_flight_detail'))


        return render_template('Staff_home.html', username = username, status = 'staff', airline_name = staff_airline_name,view_flight = view_result, start_date=start_date, end_date=end_date)
    else:
        return redirect(url_for('index'))

@app.route('/Staff/Flight_detail', methods=['GET', 'POST'])
def Staff_flight_detail():
    if 'staff' in session and 'detail_airline_name' in session and 'detail_flight_num' in session:
        username = session['staff']
        detail_airline_name = session['detail_airline_name']
        detail_flight_num = session['detail_flight_num']
        session.pop('detail_airline_name')
        session.pop('detail_flight_num')
        query1 = '''SELECT P.customer_email, T.ticket_id, P.purchase_date, P.booking_agent_id FROM ticket AS T, purchases as P \
                WHERE T.ticket_id = P.ticket_id AND T.airline_name = '{}' AND T.flight_num = '{}' '''.format(detail_airline_name,detail_flight_num)
        cursor = conn.cursor()
        cursor.execute(query1)    
        detail_result = cursor.fetchall()
        query2 = '''SELECT A.seats - COUNT(T.ticket_id) AS remaining_seats FROM airplane AS A, ticket as T, flight as F \
                WHERE F.airline_name = '{}' AND F.flight_num = {} AND F.airplane_id = A.airplane_id AND T.airline_name = F.airline_name \
                AND T.flight_num = F.flight_num '''.format(detail_airline_name,detail_flight_num)
        cursor = conn.cursor()
        cursor.execute(query2)    
        seats_result = cursor.fetchone()
        if not seats_result:
            query2 = '''SELECT A.seats AS remaining_seats FROM airplane AS A, flight as F \
                    WHERE F.airline_name = '{}' AND F.flight_num = {} AND F.airplane_id = A.airplane_id'''.format(detail_airline_name,detail_flight_num)
            cursor = conn.cursor()
            cursor.execute(query2)    
            seats_result = cursor.fetchone()
        seats_remain = seats_result['remaining_seats']
        return render_template('Staff_flight_detail.html', username = username, status = 'staff', airline_name = session['airline_name'], detail_result = detail_result, seats_remain = seats_remain, flight_num = detail_flight_num )

    else:
        return redirect(url_for('index'))

@app.route('/Staff/Add_airplane', methods=['GET', 'POST'])
def Staff_add_airplane():
    if 'staff' in session:
        username = session['staff']
        airplane_id  = request.form.get('airplane_id')
        seats = request.form.get('seats')
        if airplane_id and seats:
            query = '''SELECT airplane_id FROM airplane'''
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            for lines in result:
                if int(airplane_id) == int(lines['airplane_id']):
                    message = "Airplane ID already in system, please use a new airplane ID!"
                    return render_template('Staff_add_airplane.html', username = username, status = 'staff', airline_name = session['airline_name'], \
                        error_duplicate = message)

            query = '''INSERT INTO airplane VALUES ('{}',{},{}) '''.format(session['airline_name'],airplane_id,seats)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            message = "Successfully add plane {} with capacity of {} to system!".format(airplane_id,seats)
            return render_template('Staff_add_airplane.html', username = username, status = 'staff', airline_name = session['airline_name'], \
                add_success_message = message)
        return render_template('Staff_add_airplane.html', username = username, status = 'staff', airline_name = session['airline_name'])
    else:
        return redirect(url_for('index'))

@app.route('/Staff/Add_airport', methods=['GET', 'POST'])
def Staff_add_airport():
    if 'staff' in session:
        username = session['staff']
        airport_name  = request.form.get('airport_name')
        airport_city = request.form.get('airport_city')
        if airport_name and airport_city:
            query = '''SELECT airport_name FROM airport'''
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            for lines in result:
                if airport_name == lines['airport_name']:
                    message = "Airport Name already in system, please use a new airport name!"
                    return render_template('Staff_add_airport.html', username = username, status = 'staff', airline_name = session['airline_name'], \
                        error_duplicate = message)

            query = '''INSERT INTO airport VALUES ('{}','{}') '''.format(airport_name,airport_city)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            message = "Successfully add airport {} located at {} to system!".format(airport_name,airport_city)
            return render_template('Staff_add_airport.html', username = username, status = 'staff', airline_name = session['airline_name'], \
                add_success_message = message)
        return render_template('Staff_add_airport.html', username = username, status = 'staff', airline_name = session['airline_name'])
    else:
        return redirect(url_for('index'))

@app.route('/Staff/Create_flight', methods=['GET', 'POST'])
def Staff_create_flight():
    if 'staff' in session:
        username = session['staff']
        airline_name = session['airline_name']
        flight_num = request.form.get('flight_num')
        departure_airport = request.form.get('departure_airport')
        arrival_airport = request.form.get('arrival_airport')
        status = request.form.get('status')
        airlane_id = request.form.get('airplane_id')
        price = request.form.get('price')
        departure_time = request.form.get('departure_time')+':00'
        arrival_time = request.form.get('arrival_time')+':00'
        departure_time = departure_time.replace('T',' ')
        arrival_time = arrival_time.replace('T',' ')

        print(departure_time)
        test_time = datetime.strptime('2020-04-04 05:05:00', '%Y-%m-%d %H:%M:%S')
        print(test_time)

        if airline_name and flight_num:
            arrival_time_py = datetime.strptime(arrival_time, '%Y-%m-%d %H:%M:%S')
            departure_time_py = datetime.strptime(departure_time, '%Y-%m-%d %H:%M:%S')
            if arrival_time_py <= departure_time_py:
                message = "Departure time later than arrival time! Please re-enter."
                return render_template('Staff_create_flight.html', username = username, status = 'staff', airline_name = airline_name, \
                        error = message)
            if departure_time_py <= datetime.now().replace(microsecond=0):
                message = "Departure time earlier than right now! Please re-enter."
                return render_template('Staff_create_flight.html', username = username, status = 'staff', airline_name = airline_name, \
                        error = message)
            query = '''SELECT airport_name FROM airport'''
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            dept_ap_exist = False
            arrl_ap_exist = False
            for lines in result:
                if departure_airport == lines['airport_name']:
                    dept_ap_exist = True
                if arrival_airport == lines['airport_name']:
                    arrl_ap_exist = True
            if dept_ap_exist == False:
                message = "Departure Airport does not exist, try another!"
                return render_template('Staff_create_flight.html', username = username, status = 'staff', airline_name = airline_name, \
                        error = message)
            if arrl_ap_exist == False:
                message = "Departure Airport does not exist, try another!"
                return render_template('Staff_create_flight.html', username = username, status = 'staff', airline_name = airline_name, \
                        error = message)
            query = '''SELECT * FROM flight'''
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            for lines in result:
                if airline_name == lines['airline_name'] and int(flight_num) == int(lines['flight_num']):
                    message = "Flight number already in system, please use a new flight number!"
                    return render_template('Staff_create_flight.html', username = username, status = 'staff', airline_name = session['airline_name'], \
                        error = message)
                temp_dept_time = lines['departure_time']
                temp_arrl_time = lines['arrival_time']
                if (departure_time_py >= temp_dept_time and departure_time_py <= temp_arrl_time) or (arrival_time_py >= temp_dept_time and arrival_time_py <= temp_arrl_time):
                    time_coincide = True
                if airlane_id == lines['airplane_id'] and time_coincide:
                    message = "Airplane with ID {} already occupied in the time slot!".format(airlane_id)
                    return render_template('Staff_create_flight.html', username = username, status = 'staff', airline_name = session['airline_name'], \
                        error = message)

            query = '''INSERT INTO flight VALUES ('{}',{},'{}','{}','{}','{}',{},'{}',{} ) '''.format(airline_name,int(flight_num),departure_airport, \
                    departure_time, arrival_airport,arrival_time,Decimal(price),status, int(airlane_id))
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            message = "Successfully add flight number {} to system!".format(flight_num)
            return render_template('Staff_create_flight.html', username = username, status = 'staff', airline_name = airline_name, \
                create_success_message = message)
        return render_template('Staff_create_flight.html', username = username, status = 'staff', airline_name = airline_name)
    else:
        return redirect(url_for('index'))
    

@app.route('/Staff/Change_status', methods=['GET', 'POST'])
def Staff_change_status():
    if 'staff' in session:
        username = session['staff']
        airline_name = session['airline_name']
        flight_num  = request.form.get('flight_num')
        status = request.form.get('status')
        if flight_num and status:
            query = '''SELECT flight_num FROM flight WHERE airline_name ='{}' '''.format(airline_name)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            flight_exist = False
            for lines in result:
                if int(flight_num) == int(lines['flight_num']):
                    flight_exist = True
                    break
            if flight_exist == False:
                message = "Flight does not exist, Please confirm and re-enter!"
                return render_template('Staff_change_status.html', username = username, status = 'staff', airline_name = airline_name, \
                error = message)
            query = '''UPDATE flight SET status = '{}' WHERE flight_num = {} AND airline_name = '{}' '''.format(status,flight_num,airline_name)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            message = "Successfully changed status of flight number {} to '{}'!".format(flight_num,status)
            return render_template('Staff_change_status.html', username = username, status = 'staff', airline_name = airline_name, \
                change_success_message = message)
        return render_template('Staff_change_status.html', username = username, status = 'staff', airline_name = airline_name)
    else:
        return redirect(url_for('index'))


@app.route('/Staff/View_top_agent', methods=['GET', 'POST'])
def View_top_agent():
    if 'staff' in session:
        end_date = date.today()
        last_month = end_date + relativedelta(months=-1)
        last_year = end_date + relativedelta(months=-12)

        cursor = conn.cursor()
        #query Top five agent with number of tickets last month
        query ='''SELECT booking_agent.email, COUNT(purchases.ticket_id) FROM purchases, booking_agent, booking_agent_work_for
                WHERE booking_agent.booking_agent_id = purchases.booking_agent_id AND booking_agent.email = booking_agent_work_for.email 
                AND purchases.purchase_date >= '{}' AND booking_agent_work_for.airline_name = '{}'
                GROUP BY booking_agent.email'''.format(last_month, session['airline_name'])
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        #Select Top 5
        data = sorted(data, key=lambda x: x["COUNT(purchases.ticket_id)"], reverse=True)
        chart1_labels = [row['email'] for row in data]
        if len(chart1_labels) <= 5:
            for i in range(5-len(chart1_labels)):
                chart1_labels.append(0)
        else:
            chart1_labels = chart1_labels[:4]
        chart1_values = [row['COUNT(purchases.ticket_id)'] for row in data]
        if len(chart1_values) <= 5:
            for i in range(5-len(chart1_values)):
                chart1_values.append(0)
        else:
            chart1_values = chart1_values[:4]
        print(chart1_labels)
        print(chart1_values)

        #query Top five agent with number of tickets last year
        query ='''SELECT booking_agent.email, COUNT(purchases.ticket_id) FROM purchases, booking_agent, booking_agent_work_for
                WHERE booking_agent.booking_agent_id = purchases.booking_agent_id AND booking_agent.email = booking_agent_work_for.email 
                AND purchases.purchase_date >= '{}' AND booking_agent_work_for.airline_name = '{}'
                GROUP BY booking_agent.email'''.format(last_year, session['airline_name'])
        cursor.execute(query)
        data = cursor.fetchall()
        #Select Top 5
        data = sorted(data, key=lambda x: x["COUNT(purchases.ticket_id)"], reverse=True)
        chart2_labels = [row['email'] for row in data]
        if len(chart2_labels) <= 5:
            for i in range(5-len(chart2_labels)):
                chart2_labels.append(0)
        else:
            chart2_labels = chart2_labels[:4]
        chart2_values = [row['COUNT(purchases.ticket_id)'] for row in data]
        if len(chart2_values) <= 5:
            for i in range(5-len(chart2_values)):
                chart2_values.append(0)
        else:
            chart2_values = chart2_values[:4]
        print(chart2_labels)
        print(chart2_values)

        #query Top five agent with commissions
        query ='''SELECT booking_agent.email, SUM(flight.price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, booking_agent NATURAL JOIN booking_agent_work_for
                WHERE booking_agent.booking_agent_id = purchases.booking_agent_id AND booking_agent_work_for.airline_name = '{}' AND purchases.purchase_date >= '{}'
                GROUP BY  booking_agent.email'''.format(session['airline_name'], last_year)
        cursor.execute(query)
        data = cursor.fetchall()
        #Select Top 5
        data = sorted(data, key=lambda x: x["SUM(flight.price)"], reverse=True)
        chart3_labels = [row['email'] for row in data]
        if len(chart3_labels) <= 5:
            for i in range(5-len(chart3_labels)):
                chart3_labels.append(0)
        else:
            chart3_labels = chart3_labels[:4]
        chart3_values = [float(row['SUM(flight.price)'])*0.1 for row in data]
        if len(chart3_values) <= 5:
            for i in range(5-len(chart3_values)):
                chart3_values.append(0)
        else:
            chart3_values = chart3_values[:4]
        print(chart3_labels)
        print(chart3_values)    
        conn.commit()
        cursor.close()

        return render_template('Staff_view_top_agent.html', status='staff', airline_name = session['airline_name'],
            chart1_labels = chart1_labels, chart1_values = chart1_values,
            chart2_labels = chart2_labels, chart2_values = chart2_values,
            chart3_labels = chart3_labels, chart3_values = chart3_values
        )    
    else:
        return redirect(url_for('index'))   

@app.route('/Staff/View_customers', methods=['GET', 'POST'])
def View_customers(): 
    if "staff" in session:
        username = session['staff']
        airline_name = session['airline_name']
        today = date.today()
        start_date = today + relativedelta(years=-1)
        customer_email = request.form.get("customer_email")
        query = '''SELECT COUNT(ticket_id) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight 
                WHERE airline_name = '{}' AND purchases.purchase_date >= '{}'
                GROUP BY customer_email'''.format(airline_name,start_date,airline_name,start_date)
        cursor = conn.cursor()
        cursor.execute(query)    
        result = cursor.fetchone()
        if not result:
            top_customer_message = "There has been no customers of airline '{}' in the past year!".format(airline_name)
        else:
            query = '''SELECT customer_email FROM purchases NATURAL JOIN ticket NATURAL JOIN flight 
                    WHERE airline_name = '{}' AND purchases.purchase_date >= '{}' GROUP BY customer_email
                    HAVING COUNT(ticket_id)>=all(SELECT COUNT(ticket_id) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight 
                    WHERE airline_name = '{}' AND purchases.purchase_date >= '{}'
                    GROUP BY customer_email)'''.format(airline_name,start_date,airline_name,start_date)
            print(query)
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchone()
            top_customer_email = result['customer_email']
            top_customer_message = "The most frequent customer in the past year is '{}'!".format(top_customer_email)
        if customer_email:
            query = '''SELECT email FROM customer'''
            cursor = conn.cursor()
            cursor.execute(query)    
            result = cursor.fetchall()
            customer_exist = False
            for lines in result:
                if customer_email == lines['email']:
                    customer_exist = True
                    break
            if customer_exist == False:
                error = "Customer does not exsit, Please confirm and re-enter!"
                return render_template("Staff_view_customers.html",username = username, status = 'staff', airline_name = airline_name,top_customer_message=top_customer_message,error = error)
        
            else:
                query = '''SELECT flight_num, ticket_id, purchase_date FROM ticket NATURAL JOIN purchases WHERE customer_email = '{}' '''.format(customer_email)
                cursor = conn.cursor()
                cursor.execute(query)    
                result = cursor.fetchall()
                return render_template("Staff_view_customers.html",username = username, status = 'staff', airline_name = airline_name, top_customer_message=top_customer_message, search_result = result,customer_email = customer_email)
        else:
            return render_template("Staff_view_customers.html",username = username, status = 'staff', airline_name = airline_name,top_customer_message=top_customer_message)
    else:
        return redirect(url_for('index')) 


@app.route('/Staff/View_report', methods=['GET', 'POST'])
def View_report():
    if "staff" in session:
        end_date = date.today()
        last_month = end_date + relativedelta(months=-6)
        default = 6
        labels = []
        values = []
        #User defined range
        start_date = request.form.get('Start_date')
        if (start_date):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = request.form.get('End_date')
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if (int(end_date.year)-int(start_date.year)) == 0:
                diff = (int(end_date.month)-int(start_date.month))
            else:
                diff = (int(end_date.year)-int(start_date.year)-1)*12 + (12-int(start_date.month)+int(end_date.month))
            default = diff + 1
            print(default)

        #Data process
        cursor = conn.cursor()
        for i in range(default):
            month = (end_date + relativedelta(months=-(default-i-1))).month
            year = (end_date + relativedelta(months=-(default-i-1))).year
            labels.append(str(year)+'-'+str(month))
            print(labels)
            query = '''SELECT COUNT(ticket_id) FROM ticket NATURAL JOIN purchases WHERE airline_name = '{}' AND MONTH(purchase_date) = '{}' And YEAR(purchase_date) = '{}' '''.format(session['airline_name'], month, year)
            cursor.execute(query)
            data = cursor.fetchone()
            print(data)
            values.append(data['COUNT(ticket_id)'])
            print(values)

        conn.commit()
        cursor.close()

        return render_template('Staff_view_report.html', status='staff', airline_name = session['airline_name'],
            labels = labels ,values = values
        )
    else:
        return redirect(url_for('index'))

@app.route('/Staff/Comparison_of_Revenue', methods=['GET', 'POST'])
def Comparison_of_Revenue():
    end_date = date.today()
    last_month = end_date + relativedelta(months=-1)
    last_year = end_date + relativedelta(months=-12)

    #Query total revenue of last month
    cursor = conn.cursor()
    query ='''SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight 
            WHERE airline_name = '{}' AND booking_agent_id is Null AND purchases.purchase_date >= '{}' '''.format(session['airline_name'], last_month)
    cursor.execute(query)
    data = cursor.fetchone()
    chart1_values = []
    chart1_values.append(int(data['SUM(price)']))
    query ='''SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
            WHERE airline_name = '{}' AND booking_agent_id is not Null AND purchases.purchase_date >= '{}' '''.format(session['airline_name'], last_month)
    cursor.execute(query)
    data = cursor.fetchone()
    chart1_values.append(int(data['SUM(price)']))
    print(chart1_values)

    #Query total revenue of last year
    cursor = conn.cursor()
    query ='''SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight 
            WHERE airline_name = '{}' AND booking_agent_id is Null AND purchases.purchase_date >= '{}' '''.format(session['airline_name'], last_year)
    cursor.execute(query)
    data = cursor.fetchone()
    chart2_values = []
    chart2_values.append(int(data['SUM(price)']))
    query ='''SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
            WHERE airline_name = '{}' AND booking_agent_id is not Null AND purchases.purchase_date >= '{}' '''.format(session['airline_name'], last_year)
    cursor.execute(query)
    data = cursor.fetchone()
    chart2_values.append(int(data['SUM(price)']))
    print(chart2_values)
    conn.commit()
    cursor.close()

    return render_template('Staff_comparison_of_revenue.html',status='staff', airline_name = session['airline_name'],
    chart1_values = chart1_values, chart2_values = chart2_values
    )

@app.route('/Staff/View_top_destination', methods=['GET', 'POST'])
def View_top_destination():
    end_date = date.today()
    last_month = end_date + relativedelta(months=-3)
    last_year = end_date + relativedelta(months=-12)

    #Query Top 3 destination last month
    cursor = conn.cursor()
    query ='''SELECT airport.airport_name, COUNT(ticket.ticket_id) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, airport
        WHERE airline_name = '{}' AND flight.arrival_airport = airport.airport_name AND purchases.purchase_date >= '{}'
        GROUP BY airport.airport_name'''.format(session['airline_name'], last_month)
    cursor.execute(query)
    data = cursor.fetchall()
    data = sorted(data, key=lambda x: x["COUNT(ticket.ticket_id)"], reverse=True)
    if len(data) >= 3:
        top3_monthly = [data[i]['airport_name'] for i in range(3)]
    else:
        top3_monthly = [row['airport_name'] for row in data]
        for i in range(3-len(data)):
            top3_monthly.append(None)
    print(top3_monthly)

    #Query Top 3 destination last year
    cursor = conn.cursor()
    query ='''SELECT airport.airport_name, COUNT(ticket.ticket_id) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, airport
        WHERE airline_name = '{}' AND flight.arrival_airport = airport.airport_name AND purchases.purchase_date >= '{}'
        GROUP BY airport.airport_name'''.format(session['airline_name'], last_year)
    cursor.execute(query)
    data = cursor.fetchall()
    data = sorted(data, key=lambda x: x["COUNT(ticket.ticket_id)"], reverse=True)
    if len(data) >= 3:
        top3_annually = [data[i]['airport_name'] for i in range(3)]
    else:
        top3_annually = [row['airport_name'] for row in data]
        for i in range(3-len(data)):
            top3_annually.append(None)
    print(top3_annually)

    return render_template('Staff_view_top_destination.html', status='staff', airline_name = session['airline_name'],
    top3_monthly = top3_monthly, top3_annually = top3_annually)

@app.route('/Staff/Grant_new_permissions', methods=['GET', 'POST'])
def Grant_new_permissions():
    username = request.form.get('username')
    Admin = request.form.get('Admin') != None
    Operator = request.form.get('Operator') != None

    if request.method == "POST":
#        print(username, Admin, Operator)
        cursor = conn.cursor()
        query='''SELECT * FROM airline_staff WHERE airline_name = '{}' AND username = '{}' '''.format(session['airline_name'], username)
        cursor.execute(query)
        data = cursor.fetchone()
        if (data):
            #Give Admin permission
            if Admin:
                query='''SELECT * FROM permission WHERE username = '{}' AND permission_type = 'Admin' '''.format(username)
                cursor.execute(query)
                data = cursor.fetchone()
                if (data):
                    error = 'This user already has admin permission'
                    return render_template('Staff_Grant_new_permissions.html', status='staff', airline_name = session['airline_name'], 
                        Admin_permission = session['Admin'], error = error)
                else:
                    query = '''INSERT INTO `permission`(`username`, `permission_type`) VALUES ('{}','Admin')'''.format(username)
                    cursor.execute(query)
            #Give operator permission
            if Operator:
                query='''SELECT * FROM permission WHERE username = '{}' AND permission_type = 'Operator' '''.format(username)
                cursor.execute(query)
                data = cursor.fetchone()
                if (data):
                    error = 'This user already has operator permission'
                    return render_template('Staff_Grant_new_permissions.html', status='staff', airline_name = session['airline_name'], 
                        Admin_permission = session['Admin'], error = error)
                else:
                    query = '''INSERT INTO `permission`(`username`, `permission_type`) VALUES ('{}','Operator')'''.format(username)
                    cursor.execute(query)

        else:
            error = 'This user does not exist'
            return render_template('Staff_Grant_new_permissions.html', status='staff', airline_name = session['airline_name'], 
            Admin_permission = session['Admin'], error = error)

        conn.commit()
        cursor.close()

    return render_template('Staff_Grant_new_permissions.html', status='staff', airline_name = session['airline_name'], 
    Admin_permission = session['Admin'] )

@app.route('/Staff/Add_booking_agent', methods=['GET', 'POST'])
def Add_booking_agent():
    email = request.form.get('email')

    if request.method == "POST":
        print(email)
        cursor = conn.cursor()
        query='''SELECT * FROM booking_agent WHERE email = '{}' '''.format(email)
        cursor.execute(query)
        data = cursor.fetchone()
        #Check if the agent exist
        if (data):
            query='''SELECT * FROM booking_agent_work_for WHERE email = '{}' '''.format(email)
            cursor.execute(query)
            data = cursor.fetchone()
            #Check if the agent is authorized
            if (data):
                error = 'This agent has already been authorized'
                return render_template('Staff_Add_booking_agent.html', status='staff', airline_name = session['airline_name'], 
                Admin_permission = session['Admin'], error = error)
            else:
                query = '''INSERT INTO `booking_agent_work_for`(`email`, `airline_name`) VALUES ('{}','{}')'''.format(email, session['airline_name'])
                cursor.execute(query)

        else:
            error = 'This agent does not exist'
            return render_template('Staff_Add_booking_agent.html', status='staff', airline_name = session['airline_name'], 
            Admin_permission = session['Admin'], error = error)

        conn.commit()
        cursor.close()

    return render_template('Staff_Add_booking_agent.html', status='staff', airline_name = session['airline_name'], 
    Admin_permission = session['Admin'] )


'''----------------------------------------------------------------------------------------------------'''

#Logout
@app.route('/Logout')
def Logout():
    if 'customer' in session:
        session.pop('customer')
    elif 'agent' in session:
        session.pop('agent')
    elif 'staff' in session:
        session.pop('staff')

    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(debug=True)