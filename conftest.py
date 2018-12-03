import pytest
from app import app

@pytest.fixture(scope='module')
def test_client():
    app.cofig['TESTING']=True
    app_client=app.test_client()
    ##fails because none is returned
    ##return app_client ==works
    ctx=app.app_context()   ##sets up the particular context
    ctx.push()
    yield app_client
    ctx.pop()   ##to leave the test environment clean

def test_app(test_client):
    response=test_client.get('/')
    print(>>>>>,response) ###not sure... but print shouldhelp in debugging
    assert response.status_code==200
    assert b
    assert b'Hello Andela Code Camp' in response.data


    setting follow_rediects to True


