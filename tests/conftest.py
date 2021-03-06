import pytest
from flask import Flask
from biashara import app
from biashara.models import User

@pytest.fixture(scope='module')
def test_client():
    #flask_app = create_app('flask_test.cfg')
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    app.config['TESTING']=True
    testing_client = app.test_client()
 
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    x=User(username='Iron Man',email='ironmanrocks@gmail.com')
    y = User(username='Queen', email='kim5@gmail.com')
    db.session.add(user1)
    db.session.add(user2)
 
    # Commit the changes for the users
    db.session.commit()
 
    yield db  # this is where the testing happens!
 
    db.drop_all()

    #user1 = User(  ,email='patkennedy79@gmail.com', plaintext_password='FlaskIsAwesome')