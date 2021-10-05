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

## Running API using Docker Compose
Windows:

In a terminal window, run the following from the root dir of the project
```
cd ops
shortUrl.bat
docker-compose build
docker-compose up
``` 

Mac/Linux:

In a terminal window, run the following from the root dir of the project
```
cd ops
source shortUrl.env
docker-compose build
docker-compose up
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
    (optional) "expiration_date": "10/1/2021"
}
```
Sample Output:
```
{
  "expiration_date": "Mon, 11 Oct 2021 00:00:00 GMT",
  "id": 6,
  "last_used": null,
  "short_link": "iP7FRfML22KFxoUZYFLTRq",
  "url": "patelrohanv.com",
  "usage_count": 0
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
  "expiration_date": "Mon, 11 Oct 2021 00:00:00 GMT",
  "id": 6,
  "last_used": "Sun, 03 Oct 2021 21:52:10 GMT",
  "short_link": "iP7FRfML22KFxoUZYFLTRq",
  "url": "patelrohanv.com",
  "usage_count": 1
}
```
or
```
"short_link expired; please recreate"
```
or
```
"short_link not found"
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
    "short_link": "VuAgLPv8nhfD4qMdjFJdmu" 
}
```
Sample Output:
```
"Delete Successful"
```
or
``` 
"short_link not found"
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
    "expiration_date": "Wed, 13 Oct 2021 00:00:00 GMT",
    "id": 8,
    "last_used": "Sun, 03 Oct 2021 21:53:31 GMT",
    "short_link": "LjQPyyeoerC56CZ4cLPCGQ",
    "url": "https://github.com/patelrohanv/",
    "usage_count": 9
  },
  {
    "expiration_date": "Mon, 11 Oct 2021 00:00:00 GMT",
    "id": 6,
    "last_used": "Sun, 03 Oct 2021 21:53:56 GMT",
    "short_link": "iP7FRfML22KFxoUZYFLTRq",
    "url": "patelrohanv.com",
    "usage_count": 5
  },
  {
    "expiration_date": "Mon, 11 Oct 2021 00:00:00 GMT",
    "id": 7,
    "last_used": "Sun, 03 Oct 2021 21:54:11 GMT",
    "short_link": "HB9MXLwUwevHgro4EMHoRB",
    "url": "https://www.linkedin.com/in/patelrohanv",
    "usage_count": 3
  }
]
```

### `GET` /analytics/popular
Sample Output:
```
[
  {
    "short_link": "LjQPyyeoerC56CZ4cLPCGQ",
    "url": "https://github.com/patelrohanv/",
    "usage_count": 9
  },
  {
    "short_link": "iP7FRfML22KFxoUZYFLTRq",
    "url": "patelrohanv.com",
    "usage_count": 5
  },
  {
    "short_link": "HB9MXLwUwevHgro4EMHoRB",
    "url": "https://www.linkedin.com/in/patelrohanv",
    "usage_count": 3
  }
]
```


### `GET` /analytics/recent
Sample Output:
```
[
  {
    "last_used": "Sun, 03 Oct 2021 21:54:11 GMT",
    "short_link": "HB9MXLwUwevHgro4EMHoRB",
    "url": "https://www.linkedin.com/in/patelrohanv"
  },
  {
    "last_used": "Sun, 03 Oct 2021 21:53:56 GMT",
    "short_link": "iP7FRfML22KFxoUZYFLTRq",
    "url": "patelrohanv.com"
  },
  {
    "last_used": "Sun, 03 Oct 2021 21:53:31 GMT",
    "short_link": "LjQPyyeoerC56CZ4cLPCGQ",
    "url": "https://github.com/patelrohanv/"
  }
]
```
