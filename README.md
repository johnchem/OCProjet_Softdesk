# Download of the files
- Go to the repertory where the application will be store
- In the repertory, copy the repertory from github
`git clone https://github.com/johnchem/OCProjet_Softdesk.git`
# installation on Window
## Creation of the virtual environment
- Move into the project folder
`cd OCProjet_SoftDesk`
- Install the virtual environment
`python -m venv .env`
## Start the virtual environment
- `.env\Script\activate`
## Installation of the dependencies
- `python -m pip install -r requirements.txt.`
## launch the application
- start the virtual environment
`python -m venv .env`
- go to the project folder
`cd softdesk`
- Start the server with the command
`python manage.py runserver`
- the server is ready to receive request with the root
`http://127.0.0.1:8000/<end-point>`

# installation on Linux
## Creation of the virtual environment
- Move into the project folder
`cd OCProjet_softDesk`
- Install the virtual environment
`python3 -m venv .env`
## Start the virtual environment
- `source .env\bin\activate`
## Installation of the dependancies
- `python3 -m pip install -r requirement.py`
## launch the application
- start the virtual environment
`.env\Script\activate`
- go to the project folder
`cd softdesk`
- Start the server with the command
`python manage.py runserver`

# Run PEP8 check
les parametres de reglage sont definis dans le fichier `.flake8`

`flake8 softdesk --format=html --htmldir=flake-report`