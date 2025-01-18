Create a desired project folder, go to that path using terminal or commandline.

step 1: Cloning the project

 - git clone https://github.com/prasannadani9/ShortenUrlProject.git

step 2: Go to project and move to required branch, get the pull

 - cd ShortUrl

 - git branch -a

 - git checkout Main

 - git pull origin Main


step 3: Install the required packages and modules

 - pip install -r requirements.txt

step 4: Apply Migrations

 - py manage.py migrate

step 5: Test runserver

 - py manage.py runserver


API Documentation:

API 1 = localhost:8000/shorten/ [POST]

Description : This API is to get the shortened URL against the main long URL.

request body:

{
    "main_url" : "https://www.prasannadani9.com/jhauoevf/khqhevfu/dkjvrfa/dkagcgwcaf/kuGFUYTCRDIGKY/KFEQUTYQ/cwgvrcw/icywrygxygisyugwif",
    "expiry_in_hours" : 4
}
response body:

{
    "message": "Success",
    "data": {
        "id": 14,
        "main_url": "http://www.prasannadani9.com/jhauoevf/khqhevfu/dkjvrfa/dkagcgwcaf/kuGFUYTCRDIGKY/KFEQUTYQ/cwgvrcw/icywrygxygisyugwif",
        "short_url": "https://myshort.ly/h1QsDBUEQdCPCdHcmK8aNg/528c",
        "expiry_time": "2025-01-19T16:37:20.611354",
        "creation_time": "2025-01-18T16:37:20.616865Z"
    }
}


API 2 = localhost:8000/?short_url=https://myshort.ly/mK5VAZ9NTMy2XRF0O4z7Jw/4fad [GET]

Description : This API is to retrieve the long main URL against the created short URL.

response body:

{
    "message": "Success",
    "data": {
        "main_url": "http://www.prasannadani9.com/jhauoevf/khqhevfu/dkjvrfa/dkagcgwcaf/kuGFUYTCRDIGKY/KFEQUTYQ/cwgvrcw/icywrygxygisyugwif"
    }
}

API 3 = localhost:8000/analytics/?short_url=https://myshort.ly/QfZylnhjSfS_PccTjMrDJQ/f7d814e [GET]

Description : This API is to get the analytical data about the access to short urls provided.

response body:
{
    "message": "Success",
    "count": 3,
    "body": [
        {
            "id": 1,
            "ip_address": "127.0.0.1",
            "timestamp": "2025-01-18T09:32:44.664179Z"
        },
        {
            "id": 2,
            "ip_address": "127.0.0.1",
            "timestamp": "2025-01-18T09:34:05.146468Z"
        },
        {
            "id": 3,
            "ip_address": "127.0.0.1",
            "timestamp": "2025-01-18T09:35:08.097631Z"
        }
    ]
}
