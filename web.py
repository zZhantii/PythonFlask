def application(environ, start_response):
    headers = [('Content-type', 'text/html; charset=utf-8')]
    if environ['PATH_INFO'] == "/":
        response = "<p>Home Page</p>"
    elif environ['PATH_INFO'] == "/welcome":
        response = "<p>Welcome</p>"
    # sum
    elif environ['PATH_INFO'] == "/sum":
        params = environ['QUERY_STRING'].split('&')
        response = ""
        total_sum = 0
        for param in params:
            response += '<p>You provided the following value: ' + param + '</p>'	
            total_sum += int(param)
        response += '<p>The total sum is: ' + str(total_sum) + '</p>'
    # resta
    elif environ['PATH_INFO'] == "/resta":
        params = environ['QUERY_STRING'].split('&')
        response = ""
        total_resta = int(params[0])
        response += '<p>You provided the following value: ' + params[0] + '</p>'
        for param in params[1:]:
            response += '<p>You provided the following value: ' + param + '</p>'	
            total_resta -= int(param)
        response += '<p>The total resta is: ' + str(total_resta) + '</p>'
    # Multiplication
    elif environ['PATH_INFO'] == "/multiply":
        params = environ['QUERY_STRING'].split('&')
        response = ""
        total_multiplication = 1
        for param in params:
            response += '<p>You provided the following value: ' + param + '</p>'	
            total_multiplication *= int(param)
        response += '<p>The total multiplication is: ' + str(total_multiplication) + '</p>'
    # Division
    elif environ['PATH_INFO'] == "/divide":
        params = environ['QUERY_STRING'].split('&')
        response = ""
        total_division = int(params[0])
        response += '<p>You provided the following value: ' + params[0] + '</p>'
        for param in params[1:]:
            response += '<p>You provided the following value: ' + param + '</p>'	
            total_division /= int(param)
        response += '<p>The total division is: ' + str(total_division) + '</p>'
    else:
        response = "<p>There is no such page</p>"
    start_response('200 OK', headers)
    return [response.encode('utf-8')]

from wsgiref.simple_server import make_server

server = make_server('localhost', 9000, application)
server.serve_forever()
