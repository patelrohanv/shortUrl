## Requirements
Product Requirements:
- This URL shortener should have a well defined API for URLs created including analytics of usage
- URLs can be randomly generated (via any method you choose), or specified upon creation
- No duplicate URLs are allowed to be created
- Short links can not be easily enumerated
- Short links can expire at a future time, or can live forever
- Short links can be deleted
- If a short link is created that was once deleted, it will have no "knowledge" of its previous version

Project Requirements:
- This project should be able to be runnable locally within a docker container and some simple instructions
- This project's documentation should include build and deploy instruction
- Tests should be provided and able to be executed locally or within a test environment.

## Running API Locally

### Set up virtual env
Create the virtual environment
```
python3 -m venv path/to/venv
```

#### Activate the venv

Windows (Command Prompt):
``` 
path\to\venv\Scripts\activate.bat (cmd)

path\to\venv\Scripts\Activate.ps1 (PowerShell)
```

Mac/Linux
```
source /path/to/venv/bin/activate
```

#### Install packages
```
pip install -r requirements.txt
```

### Run App in Python
Windows:

In a terminal window, run the following from the root dir of the project
```
call ops\shortUrl.bat

docker run --rm -d^
 --name postgres^
 -e POSTGRES_USER=%POSTGRES_USER%^
 -e POSTGRES_PASSWORD=%POSTGRES_PASSWORD%^
 -e POSTGRES_DB=%POSTGRES_DB%^
 -e POSTGRES_PORT=%POSTGRES_PORT%^
 -p %POSTGRES_PORT%:%POSTGRES_PORT%^
 postgres
 
flask run
```

Mac/Linux:

In a terminal window, run the following from the root dir of the project
```
source ops/shortUrl.env

docker run --rm -d \
 --name postgres \
 -e POSTGRES_USER=$POSTGRES_USER \
 -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
 -e POSTGRES_DB=$POSTGRES_DB \
 -e POSTGRES_PORT=$POSTGRES_PORT \
 -p $POSTGRES_PORT:$POSTGRES_PORT \
 postgres
 
flask run
```

## Running API in Docker
Windows:

In a terminal window, run the following from the root dir of the project
```
ops\runApp.sh
``` 

Mac/Linux:

In a terminal window, run the following from the root dir of the project
```
ops/runApp.sh
```

## Running API using Docker Compose
Windows:

In a terminal window, run the following from the root dir of the project
```
ops\shortUrl.bat
docker-compose -f ops\docker-compose.yml build
docker-compose -f ops\docker-compose.yml up
``` 

Mac/Linux:

In a terminal window, run the following from the root dir of the project
```
source ops/shortUrl.env
docker-compose -f ops/docker-compose.yml build
docker-compose -f ops/docker-compose.yml up
```

## Running tests locally
In a terminal window, run the following from the root dir of the project (venv must be activated)
```
pytest test
```

## Running tests in Docker

## Endpoints

### `POST` /generateShortLink
Sample Input:
```
{
    "url": "patelrohanv.com",
    (optional) "expirationDate": "10/1/2021"
}
```
Sample Output:
```
{
  "expirationDate": "Fri, 01 Oct 2021 00:00:00 GMT",
  "id": 3,
  "lastUsed": null,
  "shortLink": "EvrNvFxojpyVe4dvXyNxMv",
  "url": "patelrohanv.com",
  "usageCount": 0
}
```
or
``` 
"Key patelrohanv.com already exists"
```
or
``` 
"time data '1-1-2002' does not match format '%m/%d/%Y'"
```
or
``` 
"Missing required field 'url' in request body"
```
### `Get` /{shortLink}

Sample Output:
```
{
  "expirationDate": "Sun, 03 Oct 2021 00:00:00 GMT",
  "id": 4,
  "lastUsed": "Sat, 02 Oct 2021 16:10:04 GMT",
  "shortLink": "VuAgLPv8nhfD4qMdjFJdmu",
  "url": "patelrohanv.com",
  "usageCount": 1
}
```
or
```
"shortLink expired; please recreate"
```
or
```
"shortLink not found"
```
### `DELETE` /delete/url
Sample Input:
```
{ 
    "url": "patelrohanv.com" 
}
```
Sample Output:
```
"Delete Successful"
```
or
``` 
"url not found"
```
or
```
"Missing required field 'url' in request body"
```

### `DELETE` /delete/shortLink
Sample Input:
```
{
    "shortLink": "VuAgLPv8nhfD4qMdjFJdmu" 
}
```
Sample Output:
```
"Delete Successful"
```
or
``` 
"shortLink not found"
```
or
``` 
"Missing required field 'shortLink' in request body"
```

### `DELETE` /delete/expired
Sample Output:
```
{
"Delete Successful"
}
```
### `GET` /analytics
Sample Output:
```
[
  {
    "expirationDate": "Mon, 11 Oct 2021 00:00:00 GMT",
    "id": 1,
    "lastUsed": "Sun, 03 Oct 2021 16:13:09 GMT",
    "shortLink": "LA4NqninbzWcN97fVonuDs",
    "url": "patelrohanv.com",
    "usageCount": 6
  },
  {
    "expirationDate": "Mon, 13 Dec 2021 00:00:00 GMT",
    "id": 5,
    "lastUsed": "Sun, 03 Oct 2021 16:17:34 GMT",
    "shortLink": "PKQNLAdcRGs9DqDjQWFNyM",
    "url": "https://github.com/patelrohanv/",
    "usageCount": 20
  },
  {
    "expirationDate": "Fri, 12 Nov 2021 00:00:00 GMT",
    "id": 4,
    "lastUsed": "Sun, 03 Oct 2021 16:17:48 GMT",
    "shortLink": "UrevR4pP2T3zJm4TyLLV22",
    "url": "https://www.linkedin.com/in/patelrohanv/",
    "usageCount": 9
  }
]
```

### `GET` /analytics/popular
Sample Output:
```
[
  {
    "shortLink": "PKQNLAdcRGs9DqDjQWFNyM",
    "url": "https://github.com/patelrohanv/",
    "usageCount": 20
  },
  {
    "shortLink": "UrevR4pP2T3zJm4TyLLV22",
    "url": "https://www.linkedin.com/in/patelrohanv/",
    "usageCount": 9
  },
  {
    "shortLink": "LA4NqninbzWcN97fVonuDs",
    "url": "patelrohanv.com",
    "usageCount": 6
  }
]
```


### `GET` /analytics/recent
Sample Output:
```
[
  {
    "lastUsed": "Sun, 03 Oct 2021 16:17:48 GMT",
    "shortLink": "UrevR4pP2T3zJm4TyLLV22",
    "url": "https://www.linkedin.com/in/patelrohanv/"
  },
  {
    "lastUsed": "Sun, 03 Oct 2021 16:17:34 GMT",
    "shortLink": "PKQNLAdcRGs9DqDjQWFNyM",
    "url": "https://github.com/patelrohanv/"
  },
  {
    "lastUsed": "Sun, 03 Oct 2021 16:13:09 GMT",
    "shortLink": "LA4NqninbzWcN97fVonuDs",
    "url": "patelrohanv.com"
  }
]
```
