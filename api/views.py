from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, TaskSerializer
from .models import User, Task
import jwt, datetime


class RegisterView(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoginView(APIView):

    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        #reads find the first user where the email matches
        #emails are unique because 'USERNAME_FIELD = 'email' in models
        user = User.objects.filter(email=email).first()

        #email is incorrect
        if user is None:
            raise AuthenticationFailed('Incorrect Password or Username')
        
        #password is incorrect
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password or Username')
        
        payload = {
            #this is how we determine what user this token is for
            'id': user.id,
            #this token will be kept for 1hr
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            #this is when the token is created (NOW)
            'iat': datetime.datetime.utcnow()
        }

        #new version of the syntax
        #HOW DO I USE THE SECRET IN THE SETTINGS
        token = jwt.encode(payload,'secret',algorithm='HS256')
        #this is the old version (no need to deconde anymore)
        #token = jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')

        response = Response()
        
        #this wil make it so the frontend will not have access to this cookie 
        #but it will be sent for all requests via cookies automatically
        response.set_cookie(key='jwt', value=token, httponly=True, samesite='None', secure=True)
        response.data  = {
            'jwt': token
        }

        return response

class UserView(APIView):

    def get(self, request):
        #this is how we get the cookie we want
        #cookies must be uppercase
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('Unauthenticated, and not expired')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, and expired')
        
        #find the User from the decoded jwt id and serialize it so we can send it over
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.set_cookie(key='jwt', value='', httponly=True, samesite='None', secure=True,max_age=1)
        response.data = {
            'message': 'Logged out successfully '
        }

        return response
    

#TASK Views
    
class CreateTaskView(APIView):
    #GOAL we want to create a entry in the task table 

    def post(self, request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        #we want to create a task instance with these values 
        user = User.objects.filter(id=payload['id']).first()
        title = request.data['title']
        body = request.data['body']
        is_completed = request.data['is_completed']
        completed_by = request.data['completed_by']
        task_to_save = Task(owner=user,title=title,body=body,isCompleted=is_completed,completedBy=completed_by)
        task_to_save.save()
        
        return Response({
            'message': 'task has been saved'
        })

class EditTaskView(APIView):
    #GOAL this is where can can edit title,body,isComplete or completedby
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, please Login again')
        
        task_id = request.data['id']
        title = request.data['title']
        body = request.data['body']
        is_completed = request.data['is_completed']
        completed_by = request.data['completed_by']

        foundtask = Task.objects.get(id=task_id)
        foundtask.title = title
        foundtask.body = body
        foundtask.isCompleted = is_completed
        foundtask.completedBy = completed_by

        foundtask.save()
        return Response({
            'message': 'Task has been updated'
        })

class CompleteTaskView(APIView):

    #GOAL we want to update the isCompleted boolean field
    def post(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, please Login again')
    
        taskId = request.data['id']
        foundtask = Task.objects.get(id=taskId)
        foundtask.isCompleted = True;
        foundtask.save()
        return Response({
            "message":"this task has been updated"
        })


class DeleteTaskView(APIView):
    #GOAL this is where user can delete a task that they have
    #check if this is correct
    def post(self, request):
        
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, please Login again')

        #get task id from request, find task and then delete (NOT SURE IF THIS WORKS)
        taskId = request.data['id']
        foundtask = Task.objects.get(id=taskId)
        foundtask.delete()

        return Response({
            'message': 'Task has been deleted'
        })


class GetTaskView(APIView):

    #GOAL we want to get all the task for the user
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        #find the user and get the tasks where the owner matches the user
        user = User.objects.filter(id=payload['id']).first()

        tasks = Task.objects.filter(owner=user)

        serializer = TaskSerializer(tasks, many=True)
        
        return Response({
           'data': serializer.data
        })

    
        