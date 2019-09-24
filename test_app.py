import os
import pytest
import app as flaskr

#To run tests - Command line "pytest -v"

@pytest.fixture
def client():
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()
    yield client


def test_Application_Live(client):
    """Tests whether application is live and responding"""
    response = client.get('/')
    assert response.status_code==200

def checkExists():
    """Used for test_upload, to remove entry from database so that it can be retested."""
    if flaskr.normal_db_functions.check_duplicate('instance/flaskr.sqlite','testUpload','1.1.1.1'):
        flaskr.normal_db_functions.delete_component('instance/flaskr.sqlite','testUpload','1.1.1.1')

def test_upload(client):
    """Tests whether upload works"""
    checkExists()
    response = client.post('/component?ver=1.1.1.1&Fname=testUpload',data={'file':open("README.md",'rb')},follow_redirects=True)
    assert response.status_code==200

def test_No_Duplicates(client):
    """Tries to insert same name and version that was just submitted in last test, should fail."""
    response = client.post('/component?ver=1.1.1.1&Fname=testUpload',data={'file':open("README.md",'rb')},follow_redirects=True)
    assert response.status_code==400
