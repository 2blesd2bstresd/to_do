from locust import HttpLocust, TaskSet, task
import base64

class UserBehavior(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        username = 'Max'
        password = '123'
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        self.client.post("/login", headers = {'Authorization': "Basic %s" % base64string})

    @task(1)
    def recently_viewed(self):
        self.client.get("/recently_viewed", headers = {'x-auth-token': 'e334175b-a381-4e40-9164-a15b76531814'})

    @task(2)
    def profile(self):
        self.client.get("/all_spotkeys", headers = {'x-auth-token': 'e334175b-a381-4e40-9164-a15b76531814'})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000