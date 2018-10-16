# link-shortener-sample
Currently running on https://dc2c110b.ngrok.io/. A sample web app to shorten url and redirect to original url based on python3 flask.
The html used bootstrap component jumbotron for message call. Sqlites3 are using for database to insert and select urls. I am converting the url id from database with base10 and base64 in order to encode and decode the input urls. 

## Run app
pip install flask, run 
```
python3 main.py
```

## Usage of app
The app 
1. The first time running this app, it will check the urls.lb to see if there is a table WEB_url created, if not create one.
2. User open the homepage https://dc2c110b.ngrok.io/ or http://localhost:5000(if run it on local) and submit the target url. It will route POST requests to flask app with target url. Firstly it will check the url format, add 'https://' if the url does not contain http or https, then executed sql command `INSERT INTO WEB_URL (URL) VALUES (?)` with encoded url and return id as a encoded string with host url to User.
3. When user type host url with short encoded id string, the flask app will decode the id string, executed sql query `SELECT URL FROM WEB_URL WHERE ID=?` with decoded id, get the saved url from database and redirect to target url.
