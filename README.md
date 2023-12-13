# Challenge
A database table/model "Ticket" has 1 million rows. The table has a "token" column that holds a random unique UUID value for each row, determined by Django/Python logic at the time of creation. Due to a data leak, the candidate should write a django management command to iterate over every Ticket record to regenerate the unique UUID value. The command should inform the user of progress as the script runs and estimates the amount of time remaining. The script should also be sensitive to the potentially limited amount of server memory and avoid loading the full dataset into memory all at once, and show an understanding of Django ORM memory usage and query execution. Finally, the script should ensure that if it is interrupted that it should save progress and restart near the point of interruption so that it does not need to process the entire table from the start.

1. Example Schema:
   - Model: Ticket
     - Field: ID
     - Field: Token
 
## Installation
*  Create database
    - CREATE DATABASE generate_token
    - grant all privileges on database generate_token to 'username';
* Migration
    - python manage.py makemigrations fix_regenerate
    - python manage.py migrate
* Generate UUID example
    - python bulk_insert.py
* Re-generate UUID with Django ORM
    - python manage.py regenerate_uuids --chunk-size=10000
