import unittest
from app import app, db

class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        app.config["TESTING"] = True 
        self.app = app.test_client()
        
    def tearDown(self) -> None:
        pass
    
    def test_index(self):
        res = self.app.get("/")
        self.assertEqual(res.status_code, 200)
        
        
if __name__ == "__main__":
    unittest.main(  )