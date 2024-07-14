# BasicWebServer
    This document provides an overview of a basic web server implemented using advanced Python features. It explains design choices, functionality, how to run the server, dependencies required, and includes instructions for running test units.


# Design choices: 
    *Logging requests:* Incoming requests are logged using a custom logger (requests_logger) to capture details before and after processing. This helps in tracking request information effectively.
    *Authorize requests:* Requests are authenticated using Basic authentication. A decorator checks for the presence of a valid authentication token. It returns HTTP status codes (200 for authorized, 401 for unauthorized).
    *Request handling:* The server handles incoming requests based on HTTP methods (GET, POST) and validates request syntax to ensure proper handling and response generation.
    *Creating HTTP responses manually:* HTTP responses are created manually to allow full customization of headers and content based on request details. It supports reading content from HTML files and can stream response parts using a generator.
    *Server Context Manager:* The server lifecycle is managed using a context manager (ServerContextManager). This ensures proper initialization and shutdown of the server instance, supporting synchronous and asynchronous operations.
    *Singleton Pattern Web Server:* The server is implemented using the Singleton pattern to ensure there is only one instance of the web server running at any time.

# Dependencies:
    *Python 3.12.4*
    *asyncio (for asynchronous operations)* 
    *HTML Files*

# How to run the server:
    1- Download the directory containing the webserver.py file.
    2- Open the directory in a Python-compatible IDE.
    3- Ensure all required HTML files are downloaded and placed in the same directory as webserver.py
    4- Declare your requests within the webserver.py file or provide them programmatically.
    5- Make sure Python 3.12.4 is installed.
    6- Install asyncio if not already available (pip install asyncio).
    7- Execute the webserver.py script within your IDE or from the command line.

# Testing
    *Test Requests:* 
    https://github.com/user-attachments/assets/37a841de-1f22-4cf2-a599-a03a2d4a2b3d
    
    *Test Units:* 
    https://github.com/user-attachments/assets/6c6349d1-e0b0-496b-846a-c560d000de11
    
