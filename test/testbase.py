from urllib import response
from flask_testing import TestCase
from flask import current_app, url_for

from app import app

class mainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app
    
    def test_app_exists(self):
        self.assertIsNotNone(current_app)
        
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])
        
    # def test_index_redirects(self):
    #     response= self.client.get(url_for('index'))
    #     self.assertRedirects(response, url_for('hola'))
    
    def test_hola_get(self):
        response= self.client.get(url_for('hola'))
        self.assert200(response)
        
    # def test_hola_post(self):
    #     fake_form = {
    #         'username' : 'fake',
    #         'password' : 'fake-password'
    #     }
    #     response = self.client.post(url_for('hola'), data=fake_form )
    #     self.assertRedirects(response, url_for('index'))
    
    