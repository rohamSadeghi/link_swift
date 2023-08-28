# Intro
- This Django-based URL shortener project allows you to create shortened URLs, track their usage statistics, 
and perform redirections to the original URLs. It's built using Django REST framework and provides a simple 
API for URL shortening and tracking.

### Features
- Shorten long URLs to more concise and manageable forms.
- Redirect users from the shortened URL to the original URL.
- Track usage statistics, such as the number of hits on a shortened URL.

### Installation
A. Clone the repository to your local machine:

    ``git clone https://github.com/rohamSadeghi/link_swift.git``

B. Navigate to the project directory:

``cd link_swift``

C. Create your virtual env and nstall the required packages using pip:

``pip install -r requirements.txt``

D. Run database migrations:

``python manage.py migrate``

E. Start the development server:

``python manage.py runserver``

F. Access the API using the provided endpoints.

### Endpoints

#### Shorten URL
- Endpoint: api/v1/urls/shorten/
- Method: POST
- Payload:
``  {
    "url": "https://example.com/very/long/url"
    }``
- Response: Returns a shortened URL along with its location.

#### Retrieve Shortened URL Statistics
- Endpoint: api/v1/urls/shorten/<short_code>/stats/
- Method: GET
- Response: Returns usage statistics for a specific shortened URL.

#### Redirect to Original URL
- Endpoint: api/v1/urls/shorten/<short_code>/
- Method: GET
- Action: Redirects the user to the original URL associated with the short code.

### Usage
A. Use the api/v1/urls//shorten/ endpoint to shorten a long URL by sending a POST request with the original URL.

B. Access the shortened URL using api/v1/urls/shorten/<short_code>/ endpoint to be redirected to the original URL.

C. Retrieve usage statistics for a shortened URL using api/v1/urls/shorten/<short_code>/stats/ endpoint.

### TestUrlShortenerAPI Test Cases
This test suite is designed to ensure the functionality and behavior of the URL shortener API endpoints provided by
 the Django application. It employs the Django REST framework's testing tools to perform various scenarios, including 
 URL shortening, redirection, and statistics retrieval.
 
- For running tests please run the following command:

``python manage.py test``

- For more information about the structure of test cases please check the following path:

``/link_swift/url_shortener/api/tests/test_views``


<h5>Warning</h5>
I used python3.8 as my interpreter, so for preventing broken run time issues please use the same version.
