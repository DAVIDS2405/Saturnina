from locust import HttpUser,task,between

class AppUser(HttpUser):
    wait_time = between(2,5)
        
    @task
    def login_user(self):
        payload = {
            "email": "sebastian2405lucero@hotmail.com",
            "password": "@asdaw@qweDb"
        }
        self.client.post('/api/v1/login',json=payload)