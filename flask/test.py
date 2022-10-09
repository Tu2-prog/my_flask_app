from turtle import home
import unittest
import os 
from app import Admin, User, app, db, basedir, bycrypt, Product
from flask import session
from werkzeug.utils import secure_filename


class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        
    def tearDown(self) -> None:
        pass
    
    
    def test_index(self):
        res = self.app.get("/")
        self.assertEqual(res.status_code, 200)
        
    def test_home_redirect(self):
        res = self.app.get("/home")
        self.assertEqual(res.status_code, 302)   
        
            
    def test_home(self):
        u = User(
            id = 1,
            name = "maxim",
            surname= "gomez",
            username="rehabwert22",
            password="1111"
        )
        res = self.app.post("/login", data=dict(username=u.username,
                                          password=u.password))
        self.assertEqual(res.status_code, 200)
        
    def test_log_out_redirect(self):
        res = self.app.get("/logout")
        self.assertEqual(res.status_code, 302)
        
    def test_logout(self):
        res = self.app.post("/login", data=dict(
            username="1111",
            password="1111",
            follow_redirects=True
        ))
        self.assertEqual(res.status_code, 200)
        res = self.app.get("/logout")
        self.assertEqual(res.status_code, 302)
        
    def test_admin_set_up(self):
        a = Admin(
            id=1,
            name="maxim",
            sur_name="gomez",
            admin_name="rehabwert22",
            password="1111"
        )
        db.session.add(a)
        db.session.commit()
        
        
    def test_admin_home(self):
        res = self.app.get("/admin")
        self.assertEqual(res.status_code, 200)
        
    def test_admin_set_up_form(self):
        res = self.app.get("/admin/setup")
        self.assertEqual(res.status_code, 200)
        
    def test_admin_log_in(self):
        a = Admin(
            id=1,
            name="maxim",
            sur_name="gomez",
            admin_name="rehabwert22",
            password="1111"
        )
        
        
    def test_account(self):
        res = self.app.get("/account")
        self.assertEqual(res.status_code, 302)
    
    def test_register(self):
        res = self.app.get("/register")
        self.assertEqual(res.status_code, 200)    
        
        
    def test_addproduct_form(self):
        res = self.app.get("/addproduct")
        self.assertEqual(res.status_code, 200)    
        
    
    
if __name__ == "__main__":
    unittest.main(  )