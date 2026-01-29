from locust import HttpUser, task, between

class EventsUser(HttpUser):

    # Each virtual user waits 1–3 seconds between tasks
    wait_time = between(1, 3)

    # Runs once when each user starts
    def on_start(self):
        self.headers = {
            "Content-Type": "application/json"
        }

    # Weight = 3 → executed more frequently
    @task(3)
    def view_events(self):
        with self.client.get(
            "/events?user=locust_user",
            headers=self.headers,
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure("Failed to fetch events")

    # Secondary task
    @task(1)
    def health_check(self):
        self.client.get("/health")

