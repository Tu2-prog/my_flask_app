import unittest
import os 
from app import User, app, db, basedir
from flask import session

class BaseTest(unittest.TestCase):
    """Helper functions
    """    
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
        
    def logout(self):
        return self.app.get("/logout",
                            follow_redirects=True)

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        
    def tearDown(self) -> None:
        pass
    
    
    def test_index(self):
        res = self.app.get("/")
        self.assertEqual(res.status_code, 200)
        
    def test_users_login_logout(self):
        u = User(
            id = 1,
            name = "tuan",
            surname = "tran", 
            username="gaucan", 
            password="1111")
        db.session.add(u)
        db.session.commit()
        
        rv = self.login(
            "gauncan",
            "1111", 
        )        
        self.assertEqual(rv.status_code, 200)
        rv = self.logout()
        self.assertEqual(rv.status_code, 200)
        
        
        
        
if __name__ == "__main__":
    unittest.main(  )