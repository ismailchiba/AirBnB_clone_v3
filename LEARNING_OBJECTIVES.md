# Learning Objectives

- [What REST means](#What-REST-means)
- [What API means](#What-API-means)
- [What CORS means](#What-CORS-means)
- [What is an API](#What-is-an-API)
- [What is a REST API](#What-is-a-REST-API)
- [What are other type of APIs](#What-are-other-type-of-APIs)
- [Which is the HTTP method to retrieve resource(s)](#Which-is-the-HTTP-method-to-retrieve-resource(s))
- [Which is the HTTP method to create a resource](#Which-is-the-HTTP-method-to-create-a-resource)
- [Which is the HTTP method to update resource](#Which-is-the-HTTP-method-to-update-resource)
- [Which is the HTTP method to delete resource](#Which-is-the-HTTP-method-to-delete-resource)
- [How to request REST API](#How-to-request-REST-API)

## What REST means
REST stands for Representational State Transfer. It is an architectural style for designing networked applications, particularly web services, that emphasizes a stateless client-server interaction and the use of standard HTTP methods for communication.

## What API means

API stands for Application Programming Interface. It is a set of rules, protocols, and tools that allows different software applications to communicate with each other. APIs define the methods and data formats that developers can use to interact with a software component, service, or platform, enabling them to access its functionality and data.


## What CORS means
CORS stands for Cross-Origin Resource Sharing. It is a mechanism that allows web servers to specify which origins (domains) are permitted to access the resources on a server via browsers.

When a web page makes a request to a different domain (origin) using JavaScript, the browser typically enforces the Same-Origin Policy, which prevents the web page from accessing the response if it comes from a different origin than the one that served the web page. This is a security measure to prevent certain types of attacks, such as Cross-Site Scripting (XSS).

CORS provides a way for servers to relax this restriction and explicitly allow cross-origin requests from specific origins. It works by adding HTTP headers to responses that indicate which origins are allowed to access the resources, and which types of requests (e.g., GET, POST) are allowed.
## What is an API
## What is a REST API
## What are other type of APIs

### SOAP APIs: 
- SOAP (Simple Object Access Protocol) APIs use the XML-based SOAP protocol for communication between systems. SOAP APIs define a standardized messaging format and rely on XML-based schemas for data exchange. They are often used in enterprise environments for integrating disparate systems and implementing web services.

### GraphQL APIs:
GraphQL is a query language and runtime for APIs developed by Facebook. GraphQL APIs allow clients to specify exactly what data they need in a single request, enabling more efficient data fetching and reducing over-fetching or under-fetching of data. GraphQL APIs are commonly used in modern web and mobile applications for flexible data querying.

### WebSocket APIs:
WebSocket APIs provide full-duplex communication channels over a single, long-lived connection between clients and servers. WebSocket APIs enable real-time, bidirectional communication between clients and servers, making them suitable for applications requiring low-latency, interactive features such as chat applications, online gaming, and real-time dashboards.

### RPC APIs:
RPC (Remote Procedure Call) APIs allow clients to invoke procedures or functions on remote servers as if they were local. RPC APIs abstract the complexity of network communication and remote procedure invocation, making it easier to build distributed systems. Examples of RPC frameworks include gRPC, Thrift, and Apache Avro.

### JSON-RPC and XML-RPC APIs:
JSON-RPC (JSON Remote Procedure Call) and XML-RPC (XML Remote Procedure Call) are lightweight, protocol-independent remote procedure call protocols. They enable clients to invoke methods or procedures on remote servers using JSON or XML payloads over HTTP or other transport protocols.

### RESTful APIs with Different Architectural Styles:
While REST (Representational State Transfer) is a popular architectural style for designing web APIs, there are variations and alternative architectural styles such as GraphQL, Falcor, and OData (Open Data Protocol) that offer different approaches to API design and data modeling.

## Which is the HTTP method to retrieve resource(s)
Get
## Which is the HTTP method to create a resource
Post
## Which is the HTTP method to update resource
Put (partial modification will be Patch)
## Which is the HTTP method to delete resource
Delete
## How to request REST API
To request a REST API, you typically use HTTP methods (such as GET, POST, PUT, PATCH, DELETE) to interact with the resources exposed by the API.

### 1, install requests
```bash
pip3 install requests
```
### 2, Choose the endpoint
### 3, Select the Http methods
### 4, Send a request
### 5, Handle the response

```python
import requests

# 2, Define the URL of the API endpoint
url = 'https://api.example.com/users'

# 3 and 4, Make a GET request to retrieve user data
response = requests.get(url)

# 5, Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON data
    data = response.json()
    # Process the data as needed
    print(data)
else:
    # Handle error response
    print(f'Error: {response.status_code}')

```
