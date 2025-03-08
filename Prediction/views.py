from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
import calendar
import re
# Create your views here.
def index(request):
    return render(request,"index.html")

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        username = request.POST.get('uname', '')
        email = request.POST.get('email', '')
        password = request.POST.get('psw', '')

        print(f"DEBUG: Received - {fname}, {lname}, {username}, {email}, {password}")

        if User.objects.filter(username=username).exists():
            print("DEBUG: Username already exists")
            return render(request, "signup.html", {"error": "Username already exists."})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = fname
            user.last_name = lname
            user.save()
            print("DEBUG: User created successfully")

            return redirect("signin")

        except Exception as e:
            print(f"DEBUG: Error in user creation - {e}")
            return render(request, "signup.html", {"error": "User creation failed."})

    return render(request, "signup.html")

#sign in code with all validation
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username', '')  # Use .get() to avoid KeyError
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, "signin.html", {"error": "Both fields are required."})

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("parkinson")  # Redirect to dashboard or home page
            #login(request, user)
            #return redirect('home')  # Ensure 'home' exists in urls.py
        else:
            return render(request, "signin.html", {"error": "Invalid username or password."})

    return render(request, "signin.html")


def test(request):
    city_names = { '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore', '4': 'Delhi', '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore', '8': 'Jaipur', '9': 'Kanpur', '10': 'Kochi', '11': 'Kolkata', '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai', '15': 'Nagpur', '16': 'Patna', '17': 'Pune', '18':'Surat'}

    crimes_names = { '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', '2': 'Crime against ST', '3': 'Crime against Senior Citizen', '4': 'Crime against children', '5': 'Crime against women', '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', '9':'Murder'}

    population = { '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60, '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00, '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50, '18':45.80}

    if request.method == "POST":
        city_code = request.POST['city']
        crime_code = request.POST['crime']
        year = request.POST['year']
        month = int(request.POST.get('month', 1))
        month_code = request.POST['month']  # ✅ Fetch month from form

        pop = population[city_code]
        year_diff = int(year) - 2011
        #pop = pop + 0.01 * year_diff * pop  # Adjust population
        #pop = pop * (1.01 ** year_diff)
        # Import ML libraries
        import pandas as pd
        import numpy as np
        import math
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestRegressor

        # Load dataset
        dataset = pd.read_excel(r"static/datasets/crp.xlsx", sheet_name="Sheet1")
        new_dataset = pd.read_excel(r"static/datasets/new_dataset.xlsx", sheet_name="Sheet1")

        # Encode categorical data
        le = LabelEncoder()
        new_dataset['City'] = le.fit_transform(new_dataset['City'])
        new_dataset['Type'] = le.fit_transform(new_dataset['Type'])

        x = new_dataset[new_dataset.columns[0:5]].values
        y = new_dataset['Crime Rate'].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

        model = RandomForestRegressor(random_state=0)
        model.fit(x_train, y_train)

        # ✅ Update model prediction with the new month input
        #crime_rate = model.predict([[int(year), int(city_code), pop, int(crime_code), int(month_code)]])[0]
        crime_rate = model.predict([[int(year), int(city_code), pop, int(crime_code), int(month)]])[0]

        city_name = city_names[city_code]
        crime_type = crimes_names[crime_code]
        month_name = calendar.month_name[int(month_code)]  # Convert month number to name
        if 0 <= crime_rate <= 2:
            crime_status = "Very Low Crime Area"
        elif 2 < crime_rate <= 4:
            crime_status = "Low Crime Area"
        elif 4 < crime_rate <= 15:
            crime_status = "High Crime Area"
        else:
            crime_status = "Very High Crime Area"

        # Classify crime level
        '''if crime_rate >=0 or crime_rate<=2:
            crime_status = "Very Low Crime Area"
        elif crime_rate >=2 or crime_rate<=4:
            crime_status = "Low Crime Area"
        elif crime_rate <= 15:
            crime_status = "High Crime Area"
        else:
            crime_status = "Very High Crime Area"'''
        
        cases = math.ceil(crime_rate * pop)

        return render(request, "test.html", {
            'city_name': city_name,
            'crime_type': crime_type,
            'month_name': month_name,  # ✅ Pass month name to frontend
            'year': year,
            'month':month,
            'crime_status': crime_status,
            'crime_rate': crime_rate,
            'cases': cases,
            'population': pop
        })

def parkinson(request):
    return render(request,"parkinson.html")
from django.shortcuts import render, redirect
from django.http import HttpResponse

'''from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
import calendar
import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def test(request):
    city_names = {
        '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore', '4': 'Delhi',
        '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore', '8': 'Jaipur', '9': 'Kanpur',
        '10': 'Kochi', '11': 'Kolkata', '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai',
        '15': 'Nagpur', '16': 'Patna', '17': 'Pune', '18': 'Surat'
    }

    crimes_names = {
        '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', '2': 'Crime against ST',
        '3': 'Crime against Senior Citizen', '4': 'Crime against children', '5': 'Crime against women',
        '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', '9': 'Murder'
    }

    population = {
        '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60,
        '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10,
        '12': 20.30, '13': 29.00, '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
    }

    if request.method == "POST":
        city_code = request.POST.get('city', None)
        crime_code = request.POST.get('crime', None)
        year = request.POST.get('year', None)
        month_code = request.POST.get('month', None)

        # ✅ Validate inputs
        if not (city_code and crime_code and year and month_code):
            return HttpResponse("All fields are required!", status=400)

        try:
            month_code = int(month_code)  # Ensure `month` is an integer
            year = int(year)  # Ensure `year` is an integer
        except ValueError:
            return HttpResponse("Invalid month or year format.", status=400)

        pop = population[city_code]
        year_diff = year - 2011
        pop = pop + 0.01 * year_diff * pop  # Adjust population

        # Load dataset
        dataset = pd.read_excel(r"static/datasets/crp.xlsx", sheet_name="Sheet1")
        new_dataset = pd.read_excel(r"static/datasets/new_dataset.xlsx", sheet_name="Sheet1")

        # Encode categorical data
        le = LabelEncoder()
        new_dataset['City'] = le.fit_transform(new_dataset['City'])
        new_dataset['Type'] = le.fit_transform(new_dataset['Type'])

        x = new_dataset[new_dataset.columns[0:5]].values
        y = new_dataset['Crime Rate'].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=50)

        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

        model = RandomForestRegressor(random_state=0)
        model.fit(x_train, y_train)

        # ✅ Fix the issue by using the correct `month_code`
        crime_rate = model.predict([[year, int(city_code), pop, int(crime_code), month_code]])[0]

        city_name = city_names[city_code]
        crime_type = crimes_names[crime_code]
        month_name = calendar.month_name[month_code]  # Convert month number to name

        # Classify crime level
        if crime_rate <= 1:
            crime_status = "Very Low Crime Area"
        elif crime_rate <= 5:
            crime_status = "Low Crime Area"
        elif crime_rate <= 15:
            crime_status = "High Crime Area"
        else:
            crime_status = "Very High Crime Area"

        cases = math.ceil(crime_rate * pop)

        return render(request, "test.html", {
            'city_name': city_name,
            'crime_type': crime_type,
            'month_name': month_name,
            'year': year,
            'crime_status': crime_status,
            'crime_rate': crime_rate,
            'cases': cases,
            'population': pop
        })
'''
