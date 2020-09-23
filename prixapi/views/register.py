import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .employee import Employee
from .company import Company


@csrf_exempt
def login_user(request):
    ''' Handles User authentication
    Method arg: Request -- the full HTTP request obj
    '''
    # Parses JSON string into Python dict
    req_body = json.loads(request.body.decode())
    if request.method == 'POST':

        # Use built-in 'authenticate' method to validate credentials
        # & returns a user object
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            print(token.user_id)
            # Converts obj to JSON string
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Invalid login creds; user not logged in
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles creation of new User for authentication
    Method arg: Request -- the full HTTP request obj
    '''
    # Parses JSON string into Python dict
    req_body = json.loads(request.body.decode())
    # Use django's built-in User model to create new user
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    # Creates & saves company to DB -- employee_id == NULL
    newCompany = Company.objects.create(
        name=req_body['company']
    )

    # Creates Employee instance, assigns the new company
    # to it,and saves to DB
    employee = Employee.objects.create(
        company=newCompany,
        is_admin=True,
        user=new_user
    )

    # Reassign Company's employee(FK) to above employee's id
    newCompany.employee_id = employee.id
    newCompany.save()

    # Django REST framework's built-in token generator
    token = Token.objects.create(user=new_user)

    # Return token to client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')
