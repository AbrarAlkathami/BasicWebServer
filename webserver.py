import logging
from datetime import datetime
import asyncio
import webbrowser
import os
import base64
import unittest

username = "Abrar123"
password = "Abrar123"

# Combine username and password with a colon separator
credentials = f"{username}:{password}"

# Encode in Base64
base64_credentials = base64.b64encode(credentials.encode()).decode()
print(f"Authorization: Basic {base64_credentials}")
# Configure logging once at the module level
logging.basicConfig(level=logging.DEBUG)

# Decorator that logs each incoming request
def log_request(func):
    def log_incoming_request(request, **kwargs):
        # Start the request logger
        logger = logging.getLogger('requests_logger')
        logger.debug("Incoming request...")
        log_result = func(request, **kwargs)
        logger.debug(f'Request line: {request["Request line"]}')
        logger.debug(f'Request Headers: {request["Request Headers"]}')
        logger.debug("Request processed.")
        return log_result
    return log_incoming_request

# Method to open HTML file and return its content
def open_HTML_file(file_path):
    try:
        # open the file
        with open(file_path, "r") as file:
            html_content = file.read()
            return html_content
    except FileNotFoundError:
        # can not found the file
        return 404

# Decorator that checks if a request have authorization or not + if it's authorized or not
def authorize_request(func):
    def check_authorize_request(request, *args):
        try:
            authorization_header = request["Request Headers"]["Authorization"]
            if authorization_header == "Basic QWJyYXIxMjM6QWJyYXIxMjM=":  # Replace with your actual check
                return func(200, request)
            else:
                return func(401, request)
        except KeyError:
            return func(200, request)  # No Authorization header present
    return check_authorize_request

@log_request
@authorize_request
def request_handle(status_code, request):
    if status_code != 401:
        try:
            method=request["Request line"]["Method"]
            path = request["Request line"]["Request URL"]
            request["Request line"]["HTTP Version"]
            request["Request Headers"]["User-Agent"]
            request["Request Headers"]["Host"]

            HTMLpath = str(path + ".html").replace("/", "")
            Content = open_HTML_file(HTMLpath)
            if Content == 404:
                return 404
            else:
                if method=="GET":
                    return GetRequestHandler().handle_request(request)
                elif method=="POST":
                    return PostRequestHandler().handle_request(request)
                else:
                    return 500
        except IOError:
            return 500
    else:
        return 401

# Generator that generates HTTP responses
def response_generator(status_code, request):
    if status_code == 200:
        try:

            request_headers = request["Request Body"]
            response = {
                "Status Line": {
                    "HTTP Version": request["Request line"]["HTTP Version"],
                    "Status Code": 200,
                    "Status Text": "OK"
                },
                "Response Headers": {
                    "Date: ": datetime.now(),
                    "Server: ": "ABRAR's Web Server"
                }
            }
            yield from streaming_response_generator(response)
        except KeyError:
            path = request["Request line"]["Request URL"]
            HTMLpath = str(path + ".html").replace("/", "")
            Content = open_HTML_file(HTMLpath)
            response = {
                "Status Line": {
                    "HTTP Version": request["Request line"]["HTTP Version"],
                    "Status Code": 200,
                    "Status Text": "OK"
                },
                "Response Headers": {
                    "Date: ": datetime.now(),
                    "Server: ": "ABRAR's Web Server",
                    "Content-Type: ": "text/html; charset=UTF-8",
                    "Content-Length: ": len(str(Content))
                },
                "Response Body": Content
            }
            webbrowser.open('file://'+ os.path.realpath(HTMLpath))
            yield from streaming_response_generator(response)
    elif status_code in [404, 400, 401]:
        error_pages = {
            404: "not-found.html",
            400: "Bad-Request.html",
            401: "Unauthorized-page.html"
        }
        if status_code in error_pages:
            error_file = error_pages[status_code]
            content = open_HTML_file(error_file)
            response = {
                "Status Line": {
                    "HTTP Version": request["Request line"]["HTTP Version"],
                    "Status Code": status_code,
                    "Status Text": {
                        404: "Not Found",
                        400: "Bad Request",
                        401: "Unauthorized"
                    }[status_code]
                },
                "Response Headers": {
                    "Date: ": datetime.now(),
                    "Server: ": "ABRAR's Web Server",
                    "Content-Type: ": "text/html; charset=UTF-8",
                    "Content-Length: ": len(content.encode())
                },
                "Response Body": content
            }
            webbrowser.open('file://'+ os.path.realpath(error_file))
            yield from streaming_response_generator(response)
    else:
        content = open_HTML_file("Internal-Server-Error.html")
        response = {
            "Status Line": {
                "HTTP Version": request["Request line"]["HTTP Version"],
                "Status Code": 500,
                "Status Text": "Internal Server Error"
            },
            "Response Headers": {
                "Date: ": datetime.now(),
                "Server: ": "ABRAR's Web Server",
                "Content-Type: ": "text/html; charset=UTF-8",
                "Content-Length: ": len(content.encode())
            },
            "Response Body": content
        }
        webbrowser.open('file://'+ os.path.realpath("Internal-Server-Error.html"))
        yield from streaming_response_generator(response)

# Generator that yields parts of a response incrementally
def streaming_response_generator(httpresponse):
    for element in httpresponse.items():
        yield element

class BaseRequestHandler:
    def handle_request(self, request):
        raise NotImplementedError("Subclasses must implement handle_request.")

# Derived class for GET requests
class GetRequestHandler(BaseRequestHandler):
    def handle_request(self, request):
        try:
            request["Request Body"]
            return 400
        except KeyError:
            return 200

# Derived class for POST requests
class PostRequestHandler(BaseRequestHandler):
    def handle_request(self, request):
        try:
            request["Request Body"]
            return 200
        except KeyError:
            return 400

# To manage the server's lifecycle 
class ServerContextManager:
    def __init__(self, file_name, method):
        self.file_name = file_name
        self.mode = method
        print("Start Server....")

    def __enter__(self):
        self.file_obj = open(self.file_name, self.mode)
        return self

    def __exit__(self, type, value, traceback):
        self.file_obj.close()
        print("Close Server....")

    def write(self, text):
        self.file_obj.write(text + '\n')

class WebServer:
    _instance= None
    # to create instace 
    def __new__(cls):
        # if there is no instance it will create one
        if not hasattr(cls, 'instance'):
            cls.instance = super(WebServer, cls).__new__(cls)
        return cls.instance


class RequestIterator:
    def __init__(self, requests_list):
        self.requests_list = requests_list
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.requests_list):
            request = self.requests_list[self.index]
            status_code = request_handle(request)
            response = response_generator(status_code, request)
            self.index += 1
            return response
        else:
            raise StopIteration

class AsyncRequestIterator:
    def __init__(self, requests):
        self.requests = requests

    def __aiter__(self):
        self.iter= self.responseAll()
        return self      

    async def __anext__(self):
        try:
            return await self.iter.__anext__()
        except StopAsyncIteration:
            raise StopAsyncIteration
        
    async def request_2response(self,request):
        status_code = request_handle(request)
        response= response_generator(status_code, request)
        return response

    async def responseAll(self):
        tasks = [ self.request_2response(request) for request in self.requests ]
        for task in asyncio.as_completed(tasks):
            result = await task
            yield result    

POST_Request = {
    "Request line": {
        "Method": "POST",
        "Request URL": "/example-page",
        "HTTP Version": "HTTP/1.1"
    },
    "Request Headers": {
        "Host": "www.example.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    },
    "Request Body": {
        "username": "user123",
        "password": "password123"
    }
}
Unauthorized_Request = {
    "Request line": {
        "Method": "GET",
        "Request URL": "/example-page",
        "HTTP Version": "HTTP/1.1"
    },
    "Request Headers": {
        "Host": "www.example.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Authorization": ""
    },
}
Not_Found_Request = {
    "Request line": {
        "Method": "GET",
        "Request URL": "/non-existent-page",
        "HTTP Version": "HTTP/1.1"
    },
    "Request Headers": {
        "Host": "www.example.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    },
}
Bad_Request = {
    "Request line": {
        "Method": "POST",
        "Request URL": "/example-page",
        "HTTP Version": "HTTP/1.1"
    },
    "Request Headers": {
        "Host": "www.example.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    },
}
Internal_Server_Error_Request = {
    "Request line": {
        "Method": "HEAD",
        "Request URL": "/internal-server-error",
        "HTTP Version": "HTTP/1.1"
    },
    "Request Headers": {
        "Host": "www.example.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    },
}
Authorized_Request = {
    "Request line": {
        "Method": "GET",
        "Request URL": "/example-page",
        "HTTP Version": "HTTP/1.1"
    },
    "Request Headers": {
        "Host": "www.example.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Authorization": "Basic QWJyYXIxMjM6QWJyYXIxMjM="
    },
}
Requests_list= [ Authorized_Request , Not_Found_Request, Internal_Server_Error_Request , Bad_Request , Unauthorized_Request , POST_Request]

web_server1 = WebServer()
web_server2 = WebServer()

print("Is it just one instance? ", web_server1 is web_server2)

class TestWebServer(unittest.TestCase):

    def setUp(self):
        # Setup any necessary configurations or initializations before each test
        self.Requests_list = [Authorized_Request, Not_Found_Request, Internal_Server_Error_Request, Bad_Request, Unauthorized_Request, POST_Request]

    def test_request_handle(self):
        # Test request handling for various scenarios
        for request in self.Requests_list:
            status_code = request_handle(request)
            self.assertIn(status_code, [200, 404, 400, 401, 500])

    def test_response_generator(self):
        # Test response generation for different status codes
        for request in self.Requests_list:
            status_code = request_handle(request)
            responses = list(response_generator(status_code, request))
            self.assertIsInstance(responses, list)
            self.assertGreater(len(responses), 0)

    def test_open_HTML_file(self):
        # Test the open_HTML_file function for existing and non-existing files
        content = open_HTML_file("example-page.html")
        self.assertIsNot(content, 404)  # Ensure content is not 404 when file exists

    def test_request_iterator(self):
        # Test synchronous request iterator
        iterator = RequestIterator(self.Requests_list)
        for response in iterator:
            response_list = list(response)
            self.assertIsInstance(response_list, list)


    def test_async_request_iterator(self):
        # Test asynchronous request iterator
        async def test_async_iterator():
            async for response_gen in AsyncRequestIterator(self.Requests_list):
                response_list = list(response_gen)  # Convert generator to list of tuples
                self.assertIsInstance(response_list, list)
  

        asyncio.run(test_async_iterator())



with ServerContextManager('ServerContextManager.txt', 'w') as server:
    server.write('Start Server... ')
    server.write(f'Time is {datetime.now() }')
    
    iterator = RequestIterator(Requests_list)
    for response in iterator:
        for part in response:  # Iterate over the response generator
            server.write(f"Outgoing response in noraml iterator :{part} ")
            print(part)
        print("\n\n\n")


    async def main(Requests_list):
        async for response in AsyncRequestIterator(Requests_list):
            for part in response:
                server.write(f"Outgoing response in async iterator : {part}")
                print(part)
            print("\n")

    asyncio.run(main(Requests_list))
    server.write(f'Testing units on functions: {unittest.main()}')
    server.write('Colse Server...')
    server.write('\n')

