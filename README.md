# Code - Backend

### To install dependencies

'''
pip install -r requirements.txt
'''

### To run the server

1. With gunicorn
   '''
   gunicorn --reload app:app
   '''

2. With python
   '''
   python3 app.py
   '''

### How to use gunicorn for linux

1. Starting a Gunicorn server: The basic command to start a Gunicorn server is:
   '''
   gunicorn your_app_module:app
   '''

- Replace your_app_module with the name of the Python module where your Flask application object (app) is defined.

2. Specifying the number of worker processes: You can control the number of worker processes using the -w or --workers option. For example, to start the server with 4 worker processes, use:
   '''
   gunicorn -w 4 your_app_module:app
   '''

3. Setting the bind address and port: The -b or --bind option allows you to specify the address and port on which the server should bind. For example, to bind to localhost on port 8000, use:
   '''
   gunicorn -b localhost:8000 your_app_module:app
   '''

- Logging options: Gunicorn provides various options to configure logging. For example, you can set the log level using the --log-level option. The available log levels are debug, info, warning, error, and critical. To set the log level to info, use:

5. gunicorn --log-level info your_app_module:app

- Graceful shutdown: To gracefully shutdown the Gunicorn server, send a SIGTERM or SIGINT signal to the process. For example, you can use Ctrl+C in the terminal where the server is running to send the SIGINT signal and initiate a graceful shutdown.
