# SharpShort URL Shorting Service

#### Infrastructure
* Development: use Docker + docker-compose
* Production: deploy to Heroku  https://sharpshort.herokuapp.com/


#### Setup instruction
* Install Docker and docker-compose on the system
* Run `docker-compose up` to start the server
* Run `docker exec -it sharpshort-backend bash` to go inside the running container
* Inside container, Run `python manage.py migrate` to apply migrations


#### API System
* Use RESTful API


#### URL Shortening Feature
https://sharpshort.herokuapp.com/
* Support more than 90 million URLs
* Pre-generate empty paths to avoid massive concurrent requests
* Always lock 1 row on the table before update to avoid accessing simultaneously
* The shortening path is fixed length with 5 characters
* The frontend page is using HTML + CSS + Javascript + JQuery
* The way to shorten URLs is calling the backend API asynchronously
* The API will store the destination URL with the pre-generated path on `Shorting` table
* If the input URL is invalid, the backend will return an error message.
  The frontend will also show the message in red to notice the user.


#### URL Redirection Preview Feature
https://sharpshort.herokuapp.com/preview/<path\>/
* The view is rendered directly by the backend with the corresponding information.
* Users can see what is the destination URL of this path


#### URL Redirection Feature
https://sharpshort.herokuapp.com/<path\>/
* Find the <path\> on `Shorting` table and redirect the user to the destination
* If the path doesn't exist, return error message with status code 404


#### Test Coverage
* `TestShortingModel`: Test pre-generate URLs
* `TestShorteningAPI`: Simulate HTTP request to verify Shortening API call and URL redirection
