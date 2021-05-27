# Bank-management-system

##Add the tables in the database

We can add the tables in the database in two methods:

1-By running these commands: 

    from app import db;
    from app.model import user;
    from app.model import bank_account;
    from app.mddel import account_transaction_details;
But, if we want to add new column in the table we have to drop all the tables and the data is also lost.

2.Using the flask-script and flask-migrate:

###Installation of flask-script and flask-migrate:
     pip install flask-script;
     pip install flask-migrate;

Import these in the init.py and run.py and it handles the database migration by running the migration commands.

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

##-Have made the collection of APIs in postman


 https://www.getpostman.com/collections/c49ee49f5cf73a8b014a


        