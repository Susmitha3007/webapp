from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.authtoken.models import Token
from app.models import Destination


# Create your views here.


class Postman(APIView):
    """
    A class to handle API requests by forwarding them to a specified URL 
    with given HTTP method, headers, and parameters.

    Methods
    -------
    post(request: Request):
        Processes the incoming request, validates it, and forwards it to 
        the specified URL using the specified HTTP method. Returns the 
        response from the forwarded request.
    """

    def post(self, request: Request):
        """
        Handles POST requests to forward them to a specified URL.

        Parameters
        ----------
        request : Request
            The incoming request object containing data with keys "url", 
            "http_method", "headers", and "params".

        Returns
        -------
        Response
            A Response object containing the result of the forwarded request 
            or an error message if the request is invalid.

        Raises
        ------
        Response
            If the URL is missing or invalid, or if the HTTP method is missing, 
            returns a Response object with a relevant error message and a 400 status code.
            If authorization credentials are missing or invalid, returns a Response 
            object with a relevant error message and a 400 status code.
        """
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
    """
    A class to handle the creation of Destination objects by processing 
    incoming POST requests.

    Methods
    -------
    post(request: Request):
        Processes the incoming request, validates it, and creates a new 
        Destination object with the provided data.
    """
    def post(self, request: Request):
        """
        Handles POST requests to create a new Destination.

        Parameters
        ----------
        request : Request
            The incoming request object containing data with keys "url", 
            "http_method", and "headers".

        Returns
        -------
        Response
            A Response object containing a success message if the 
            Destination is created successfully, or an error message 
            if the request is invalid or if there is an error during 
            the creation of the Destination.

        Raises
        ------
        Response
            If the URL is missing or invalid, or if the HTTP method is missing, 
            returns a Response object with a relevant error message and a 400 status code.
            If authorization credentials are missing or invalid, returns a Response 
            object with a relevant error message and a 400 status code.
            If there is an error while creating the Destination object, returns a 
            Response object with a relevant error message and a 400 status code.
        """

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
    """
    A class to handle viewing Destination objects for the authenticated user.

    Methods
    -------
    get(request: Request):
        Retrieves and returns a list of Destination objects associated with 
        the authenticated user.
    """

    def get(self, request:Request):
        """
        Handles GET requests to retrieve Destination objects for the authenticated user.

        Parameters
        ----------
        request : Request
            The incoming request object.

        Returns
        -------
        Response
            A Response object containing a list of Destination objects for the 
            authenticated user. If no Destination objects are found, an empty list 
            is returned.
        """
        destination_objs = Destination.objects.filter(user=request.user)
        if destination_objs:
            destination_objs = list(destination_objs.values())
        else:
            destination_objs = []
        return Response(destination_objs)
    
class ViewDetailDestination(APIView):
    """
    A class to handle viewing the detailed information of a specific 
    Destination object based on its ID.

    Methods
    -------
    get(request: Request):
        Retrieves and returns the detailed information of a Destination 
        object based on the provided ID.
    """

    def get(self, request:Request):
        """
        Handles GET requests to retrieve detailed information of a specific 
        Destination object.

        Parameters
        ----------
        request : Request
            The incoming request object containing query parameters with the key "id".

        Returns
        -------
        Response
            A Response object containing the detailed information of the specified 
            Destination object. If the ID is not provided or invalid, an appropriate 
            error message and status code are returned.

        Example
        -------
        To use this endpoint, the request should include a query parameter with the 
        key "id" indicating the ID of the Destination object to be retrieved. For example:

            GET /api/view-detail-destination?id=123

        This request will return the details of the Destination object with ID 123.
        """
        query_params = request.query_params
        id = query_params.get("id")
        destination_objs = list(Destination.objects.filter(id=int(id)).values())
        return Response(destination_objs)
        

class EditDestination(APIView):
    """
    A class to handle editing existing Destination objects.

    Methods
    -------
    post(request: Request):
        Processes the incoming request, validates it, and updates the 
        specified Destination object with the provided data.
    """
    def post(self, request:Request):
        """
        Handles POST requests to edit an existing Destination.

        Parameters
        ----------
        request : Request
            The incoming request object containing data with keys "id", 
            "url", "http_method", and "headers".

        Returns
        -------
        Response
            A Response object containing a success message if the 
            Destination is updated successfully, or an error message 
            if the request is invalid or if there is an error during 
            the update of the Destination.

        Raises
        ------
        Response
            If the URL is missing or invalid, or if the HTTP method is missing, 
            returns a Response object with a relevant error message and a 400 status code.
            If authorization credentials are missing or invalid, returns a Response 
            object with a relevant error message and a 400 status code.
            If there is an error while updating the Destination object, returns a 
            Response object with a relevant error message and a 400 status code.

        Example
        -------
        To use this endpoint, the request should include data with the keys 
        "id", "url", "http_method", and "headers". For example:

            POST /api/edit-destination
            {
                "id": 123,
                "url": "https://example.com",
                "http_method": "GET",
                "headers": {"Authorization": "Token exampletoken"}
            }

        This request will update the Destination object with ID 123 with the new URL, 
        HTTP method, and headers.
        """
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
    """
    A class to handle deleting a specific Destination object based on its ID.

    Methods
    -------
    get(request: Request):
        Deletes the Destination object specified by the ID provided in the 
        query parameters of the GET request.
    """
    
    def get(self, request:Request):
        """
        Handles GET requests to delete a specific Destination object.

        Parameters
        ----------
        request : Request
            The incoming request object containing query parameters with the key "id".

        Returns
        -------
        Response
            A Response object confirming the successful deletion of the specified 
            Destination object. If the ID is not provided or invalid, an appropriate 
            error message and status code are returned.

        Example
        -------
        To use this endpoint, the request should include a query parameter with the 
        key "id" indicating the ID of the Destination object to be deleted. For example:

            GET /api/delete-destination?id=123

        This request will delete the Destination object with ID 123.
        """
        id = request.query_params.get("id")
        delete_des =  Destination.objects.delete(id=int(id))
        return Response({
            "message" : "Destination deleted successfully"
        })


class RunDestination(APIView):
    """
    A class to handle running Destination objects by making HTTP requests 
    to specified URLs with specified HTTP methods, headers, and parameters.

    Methods
    -------
    run_destination(url: str, http_method: str, headers: dict, params: dict = {}) -> dict:
        Makes an HTTP request to the specified URL using the specified HTTP method, headers, 
        and parameters. Returns a dictionary with a status indicating success or failure, 
        and an optional error message in case of failure.

    get(request: Request) -> Response:
        Retrieves Destination objects associated with the authenticated user and attempts 
        to run each one using the `run_destination` method. Returns a success message if 
        all destinations are run successfully, otherwise returns an error message.

    Attributes
    ----------
    None
    """
    
    def run_destination(self,url,http_method,headers,params={}):
        """
        Makes an HTTP request to the specified URL using the specified HTTP method, headers, 
        and parameters.

        Parameters
        ----------
        url : str
            The URL to send the HTTP request to.
        http_method : str
            The HTTP method to use (e.g., 'GET', 'POST', 'PUT').
        headers : dict
            The headers to include in the HTTP request.
        params : dict, optional
            The parameters to include in the HTTP request payload, by default {}.

        Returns
        -------
        dict
            A dictionary with two keys:
                - 'status': A boolean indicating whether the request was successful (True) or not (False).
                - 'error': An optional error message in case of failure, or None if successful.
        """
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
        """
        Handles GET requests to retrieve and run Destination objects for the authenticated user.

        Parameters
        ----------
        request : Request
            The incoming request object.

        Returns
        -------
        Response
            A Response object containing a success message if all Destination objects are run 
            successfully, or an error message if any error occurs during the running of 
            Destination objects.
        """
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
            return Response({"Message":"Error while running destianation","Error":response.get("error")}, status=400)
        



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


