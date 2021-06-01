# Bank-management-system

##Version:
  * Project have the version as:
    
    Python 3.8.5
##Virtual Environment:

* ### Install virtual environment:
  * If you have  added any additional package in project then you can create new requirements file
  * For venv we need to install the command in required directory we want:
   
        $ pip install virtualenv
    
* ### Activate virtual environment:
  * After installation to activate the venv use command:


    source /home/siddhesh/PycharmProjects/Project/venv/bin/activate

##Install Requirement.txt:
 * To install requirement.txt activate the venv and the path where need to be installed with following command:
       
        pip freeze > requirement.txt

##Installations of the packages:
 * As we have requirement.txt added, it have all the required packages for this system need to run only this command for installations
   
        pip install -r requirements.txt

## Adding the tables in the database:
 * We need the flask-script and flask-migrate.

##Migration commands

    flask db init
Creates a new migration repository.    

    flask db migrate
Autogenerate a new revision file

    flask db upgrade
Upgrade to a later version

##Use of flask-script and flask-migrate:
- Using these data migration is done and we can add new column in the table using migration commands without losing any data
- And, can also create table or update it without dropping all the tables.

## Postman collection of the APIs:
  * Have added the postman collection json file in the git repo.
    

    cd /home/siddhesh/PycharmProjects/Project/Bank management system.postman_collection.json

