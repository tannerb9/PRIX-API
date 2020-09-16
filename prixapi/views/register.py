import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .employee import Employee


@csrf_exempt
def login_user(request):
    ''' HANDLES USER AUTHENTICATION
    METHOD ARGS: REQUEST -- THE FULL HTTP REQUEST OBJ
    '''

    # PARSES JSON STRING INTO PYTHON DICT
    req_body = json.loads(request.body.decode())

    # IF REQUEST IS HTTP POST, HANDLE VALIDATION
    if request.method == 'POST':

        # USE BUILT-IN 'AUTHENTICATE' METHOD TO VALIDATE CREDS
        # & RETURNS A USER OBJECT
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            # CONVERTS OBJ TO JSON STRING
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # INVALID LOGIN CREDS; USER NOT LOGGED IN
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''HANDLES CREATION OF NEW USER FOR AUTH
    METHOD ARGS: REQUEST -- FULL HTTP REQUEST OBJ
    '''

    # PARSES JSON STRING INTO PYTHON DICT
    req_body = json.loads(request.body.decode())

    # USES DJANGO'S BUILT-IN USER MODEL TO CREATE NEW USER
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    # CREATES AND SAVES COMPANY TO DB -- EMPLOYEE_ID == NULL
    company = Company.objects.create(
        name=req_body['name']
    )

    # CREATES AND SAVES EMPLOYEE TO DB
    employee = Employee.objects.create(
        company=req_body['company'],
        is_admin=req_body['is_admin'],
        user=new_user
    )

    # SAVES NEWLY CREATED EMPLOYEE'S ID TO THE NEW COMPANY INSTANCE
    company.employee_id = employee.id
    company.save()

    # USE REST FRAMEWORK'S TOKEN GENERATOR
    token = Token.objects.create(user=new_user)

    # RETURN TOKEN TO CLIENT
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')
