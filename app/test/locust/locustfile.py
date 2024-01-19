from locust import HttpUser,task,between

class AppUser(HttpUser):
    wait_time = between(2,5)
        
    @task
    def get_products(self):
        self.client.get('/api/v1/products')
        
    @task
    def get_category(self):
        self.client.get('/api/v1/category')
    @task
    def get_id_product(self):
        self.client.get('/api/v1/products/product:7skiqnlf2fjkyts0cllt',)
