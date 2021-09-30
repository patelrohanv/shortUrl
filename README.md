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

## Running Locally
### Set up virtual env
Create the virtual environment
```
python3 -m venv path/to/venv
```

### Activate the venv

Windows (Command Prompt):
``` 
path\to\venv\Scripts\activate.bat (cmd)

path\to\venv\Scripts\Activate.ps1 (PowerShell)
```

Mac/Linux
```
source /path/to/venv/bin/activate
```

### Install packages
```
pip install -r requirements.txt
```

### Run 
Windows:

In a terminal window, run the following from the root dir of the project
```
ops\postgres.bat
flask run
```

Mac/Linux:

In a terminal window, run the following from the root dir of the project
```
ops/postgres.sh
flask run
```

## Running in Docker
Windows:

In a terminal window, run the following from the root dir of the project
```
docker-compose -f ops\docker-compose.yml build
docker-compose -f ops\docker-compose.yml up
``` 

Mac/Linux:

In a terminal window, run the following from the root dir of the project
```
docker-compose -f ops/docker-compose.yml build
docker-compose -f ops/docker-compose.yml up
```