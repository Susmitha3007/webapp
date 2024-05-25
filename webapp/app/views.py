from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.authtoken.models import Token
from app.models import Destination


# Create your views here.


class Postman(APIView):

    def post(self, request: Request):
        query_params = request.data
        url = query_params.get("url")
        http_method = query_params.get("http_method")
        headers = query_params.get("headers")
        params = query_params.get("params")

        if url:
            if not url.startswith("http") and not url.startswith("https"):
                return Response({"error": "Invalid url"}, status=400)
        else:
            return Response({"error": "Url not found"}, status=400)

        if not http_method:
            return Response({"error": "Method not found"}, status=400)

        if headers:
            token_data = headers.get("Authorization")
            token = token_data.split(" ")[1] if token_data else None
            print("token", token)

            token_objs = Token.objects.filter(key=token)

            if not token_objs:
                return Response(
                    {"error": "Authorization credentials not found"}, status=400
                )

        if http_method.lower() == "get":
            response = requests.get(url, headers=headers, params=params)
        elif http_method.lower() in ["post", "put"]:
            response = requests.request(http_method, url, headers=headers, json=params)
        print("response", response.status_code)
        json_data = dict(response.json())
        print(json_data)
        return Response({"result": json_data})


class CreateDestination(APIView):

    def post(self, request: Request):
        query_params = request.data
        url = query_params.get("url")
        http_method = query_params.get("http_method")
        headers = query_params.get("headers")
        
        
        if url:
            if not url.startswith("http") and not url.startswith("https"):
                return Response({"error": "Invalid url"}, status=400)
        else:
            return Response({"error": "Url not found"}, status=400)

        if not http_method:
            return Response({"error": "Method not found"}, status=400)

        if headers:
            token_data = headers.get("Authorization")
            token = token_data.split(" ")[1] if token_data else None
            print("token", token)

            token_objs = Token.objects.filter(key=token)

            if not token_objs:
                return Response(
                    {"error": "Authorization credentials not found"}, status=400
                )
                
        user =  request.user
        try:
            Destination.objects.create(
                user = user,
                url = url,
                http_method = http_method,
                headers = headers
            )
        except:
            return Response({"error":"Error while creating destination"},status=400)
        
        return Response({"message":"Destination created"})
    
    
class ViewDestination(APIView):

    def get(self, request:Request):
        destination_objs = Destination.objects.filter(user=request.user)
        if destination_objs:
            destination_objs = list(destination_objs.values())
        else:
            destination_objs = []
        return Response(destination_objs)
    
class ViewDetailDestination(APIView):

    def get(self, request:Request):
        query_params = request.query_params
        id = query_params.get("id")
        destination_objs = list(Destination.objects.filter(id=int(id)).values())
        return Response(destination_objs)
        

class EditDestination(APIView):
    
    def post(self, request:Request):
        query_params = request.data
        id = query_params.get("id")
        url = query_params.get("url")
        http_method = query_params.get("http_method")
        headers = query_params.get("headers")
        
        
        if url:
            if not url.startswith("http") and not url.startswith("https"):
                return Response({"error": "Invalid url"}, status=400)
        else:
            return Response({"error": "Url not found"}, status=400)

        if not http_method:
            return Response({"error": "Method not found"}, status=400)

        if headers:
            token_data = headers.get("Authorization")
            token = token_data.split(" ")[1] if token_data else None
            print("token", token)

            token_objs = Token.objects.filter(key=token)

            if not token_objs:
                return Response(
                    {"error": "Authorization credentials not found"}, status=400
                )
                
        try:
            des_data = Destination.objects.get(id=id)
            if des_data:
                des_data.url = url
                des_data.http_method = http_method
                des_data.headers = headers
                des_data.save()
            
        except:
            return Response({"error":"Error while creating destination"},status=400)
        
        return Response({"message":"Destination created"})
    

class DeleteDestination(APIView):
    
    def get(self, request:Request):
        id = request.query_params.get("id")
        delete_des =  Destination.objects.delete(id=int(id))
        return Response({
            "message" : "Destination deleted successfully"
        })


class RunDestination(APIView):
    
    def run_destination(self,url,http_method,headers,params={}):
        error = None
        try:
            if http_method.lower() == "get":
                response = requests.get(url, headers=headers, params=params)
            elif http_method.lower() in ["post", "put"]:
                response = requests.request(http_method, url, headers=headers, json=params)
        except Exception as e:
            error = {"error": e}
        
        if error:
            return {"status": False,"error":error}
        else:
            return {"status": True}
        
        
    
    def get(self,request:Request):
        params = request.query_params.get("params")
        destination_objs = Destination.objects.filter(user=request.user).values()
        if destination_objs:
            for destination in destination_objs:
                response = self.run_destination(
                    url=destination.get("url"),
                    http_method=destination.get("http_method"),
                    headers=destination.get("headers"),
                    params=params,
                )
        if response:
            return Response({"Message":"Destination loaded successfully"})
        else:
            return Response({"Message":"Error while running destianation","Error":response.get("error")})
        



class Articles(APIView):

    def get(self, request: Request):
        query_params = request.query_params
        name = query_params.get("name")
        place = query_params.get("place")
        data = {
            "name": name,
            "place": place,
        }
        return Response(data)

    def post(self, request: Request):
        query_params = request.data
        email = query_params.get("email")
        members = query_params.get("members")
        data = {"email": email, "members": members}
        return Response(data)


