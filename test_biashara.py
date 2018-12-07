import os

import tempfile
import pytest
from biashara.control import app


@pytest.fixture
def client():
    db_fd, biashara.app.config['DATABASE'] = tempfile.mkstemp()
    biashara.app.config['TESTING']=True
    client = biashara.app.test_client()
    with biashara.app.app_context():
        biashara.init_db()
        flaskr.init_db()
    
    yield client
    
    os.close(db_fd)
    os.unlink(biashara.app.config['DATABASE'])

    ##flaskr.app.app_context()
    ##flaskr.app.test_client()
    ##flaskr.app.config['TESTING'] = True
