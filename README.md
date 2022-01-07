# P10 -SoftDest
 API collection for project support, managing teams and issues

# Setup virtual environment
python3.5 -m venv venv/

# Activate virtual environment
source venv/bin/activate

# Clone project
git clone https://github.com/Neurodium/P10-SoftDesk.git

# Install dependencies
run pip install -r src/requirements.txt

# Initialize database
 run manage.py migrate

# Launch Server
run manage.py runserver

# Django application access
Get the API collection from Postman:  https://documenter.getpostman.com/view/17160432/UVXdQf8o
Import the collection in your respository

# Features: Endpoint list:
1. [Register] HTTP METHOD: POST: http://127.0.0.1:8000/signup/<br>
&nbsp;&nbsp;Create your account
  
2. [Login] HTTP METHOD: POST: http://127.0.0.1:8000/login/<br>
&nbsp;&nbsp;Log into your account with your credentials 
  
3. [User Projects list] HTTP METHOD: GET: http://127.0.0.1:8000/projects/<br>
&nbsp;&nbsp;List of projects where user is author or contributor
  
4. [Create Project] HTTP METHOD: POST: http://127.0.0.1:8000/projects/<br>
&nbsp;&nbsp;Create a project
  
5. [Get Project Details] HTTP METHOD: http://127.0.0.1:8000/abonnements/<br>
&nbsp;&nbsp;Manage the users you want to follow

[YourUsername] http://127.0.0.1:8000/password-change/<br>
&nbsp;&nbsp;Change your password
  
[Se déconnecter] http://127.0.0.1:8000/logout/<br>
&nbsp;&nbsp;Disconnect from website
