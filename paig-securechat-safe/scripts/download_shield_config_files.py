import requests
import json

class ShieldConfigDownloader:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = self.create_authenticated_session()

    def create_authenticated_session(self):
        """Authenticate and return a session with active login."""
        session = requests.Session()
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        login_payload = json.dumps({
            "username": self.username,
            "password": self.password
        })

        login_api = f"{self.base_url}/account-service/api/login"
        response = session.post(login_api, headers=headers, data=login_payload, verify=False)

        if response.status_code == 200:
            return session
        else:
            raise Exception(f"Login failed: {response.status_code}, {response.text}")

    def fetch_ai_applications(self):
        """Fetch the list of AI applications."""
        url = f"{self.base_url}/governance-service/api/ai/application?size=15&sort=createTime,desc"
        response = self.session.get(url, verify=False)
        if response.status_code == 200:
            return response.json().get("content", [])
        else:
            print(f"Failed to fetch applications: {response.status_code}")
            return []

    def download_ai_application_shield_configs(self, required_app_names, download_path):
        """Ensure 'Plant Operations' and 'Plant Operations Unsafe' exist."""
        existing_apps = self.fetch_ai_applications()
        existing_apps_dict = {app["name"]:app for app in existing_apps}

        for app_name in required_app_names:
            if app_name in existing_apps_dict:
                app_id = existing_apps_dict[app_name]["id"]
                response = self.session.get(f"{self.base_url}/governance-service/api/ai/application/{app_id}/config/json/download", verify=False)
                if response.status_code == 200:
                    file_name = "privacera-shield-" + app_name.replace(" ", "-") + "-config.json"
                    with open(f"{download_path}/{file_name}", "w") as f:
                        f.write(json.dumps(response.json(), indent=4))
                    print(f"Shield config for {app_name} downloaded successfully.")
                else:
                    print(f"Failed to download shield config for {app_name}: {response.status_code}, {response.text}")
            else:
                print(f"Application '{app_name}' does not exist.")

if __name__ == "__main__":
    BASE_URL = "http://paig-opensource-container:4545"
    USERNAME = "admin"
    PASSWORD = "welcome1"

    REQUIRED_SHIELD_CONFIG_DOWNLOAD_APPS = ["IT Support - Safe", "Plant Operations - Safe", "Sales Intel - Safe"]

    client = ShieldConfigDownloader(BASE_URL, USERNAME, PASSWORD)
    client.download_ai_application_shield_configs(REQUIRED_SHIELD_CONFIG_DOWNLOAD_APPS, "/opt/paig/custom-configs")
