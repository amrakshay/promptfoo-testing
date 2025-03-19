import requests
import json

class DemoDataClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = self.create_authenticated_session()
        self.existing_metadata = {}
        self.existing_vectordbs = {}
        self.existing_ai_apps = {}

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

    def fetch_groups(self, size=100):
        """Fetch all groups using the authenticated session."""
        groups_api = f"{self.base_url}/account-service/api/groups?page=0&size={size}&sort=createTime,desc"

        try:
            response = self.session.get(groups_api, verify=False)
            if response.status_code == 200:
                return response.json().get("content", [])  # Return list of groups
            else:
                print(f"Error fetching groups: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Failed to fetch groups: {e}")
            return []

    def create_group(self, group_name):
        """Create a new group if it does not exist."""
        create_api = f"{self.base_url}/account-service/api/groups"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        payload = {
            "name": group_name,
            "description": "",
            "status": 1,
            "delUsers": [],
            "addUsers": [],
            "groupName": group_name
        }

        response = self.session.post(create_api, headers=headers, json=payload, verify=False)

        if response.status_code == 201:
            print(f"Group '{group_name}' created successfully.")
        else:
            print(f"Failed to create group '{group_name}': {response.status_code}, {response.text}")

    def ensure_groups_exist(self, required_groups):
        """Ensure that all required groups exist."""
        existing_groups = {group["name"] for group in self.fetch_groups()}
        missing_groups = set(required_groups) - existing_groups

        for group in missing_groups:
            self.create_group(group)

    def fetch_users(self):
        """Fetch existing users."""
        response = self.session.get(f"{self.base_url}/account-service/api/users?page=0&size=100&sort=createTime,desc", verify=False)
        if response.status_code == 200:
            return {user["username"]: user for user in response.json().get("content", [])}
        print("Failed to fetch users:", response.text)
        return {}

    def create_user(self, username, groups):
        """Create a new user."""
        payload = {
            "firstName": username,
            "lastName": "",
            "email": "",
            "username": username,
            "password": "Welcome@123456",
            "roles": ["USER"],
            "status": 1,
            "userInvited": False,
            "groups": groups
        }
        response = self.session.post(f"{self.base_url}/account-service/api/users", json=payload, verify=False)
        if response.status_code == 201:
            print(f"User '{username}' created successfully.")
        else:
            print(f"Failed to create user '{username}':", response.text)

    def update_user_groups(self, user_id, username, groups):
        """Update user groups if they do not match expected values."""
        payload = {
            "groups": groups
        }
        response = self.session.put(f"{self.base_url}/{user_id}/groups", json=payload, verify=False)
        if response.status_code == 200:
            print(f"User '{username}' groups updated successfully.")
        else:
            print(f"Failed to update groups for '{username}':", response.text)

    def ensure_users_exist(self, required_users):
        """Ensure expected users exist with the correct groups."""
        existing_users = self.fetch_users()

        for username, expected_groups in required_users.items():
            if username in existing_users:
                user = existing_users[username]
                current_groups = user.get("groups", [])
                if set(current_groups) != set(expected_groups):
                    self.update_user_groups(user["id"], username, expected_groups)
            else:
                self.create_user(username, expected_groups)

    def fetch_metadata_keys(self):
        """Fetch existing metadata keys and store them in self.existing_metadata"""
        response = self.session.get(
            f"{self.base_url}/account-service/api/vectordb/metadata/key?size=50"
        )
        if response.status_code == 200:
            data = response.json()
            self.existing_metadata = {item["name"]: item["id"] for item in data.get("content", [])}
        else:
            raise Exception(f"Failed to fetch metadata keys: {response.text}")

    def create_metadata_key(self, name):
        """Create a new metadata key and update self.existing_metadata"""
        response = self.session.post(
            f"{self.base_url}/account-service/api/vectordb/metadata/key",
            json={"type": "USER_DEFINED", "name": name, "valueDataType": "multi_value", "description": ""}
        )
        if response.status_code == 201:
            metadata = response.json()
            self.existing_metadata[name] = metadata["id"]
        else:
            raise Exception(f"Failed to create metadata key {name}: {response.text}")

    def ensure_metadata_keys_exist(self, required_metadata):
        """Ensure all required metadata keys exist"""
        self.fetch_metadata_keys()
        for key in required_metadata.keys():
            if key not in self.existing_metadata:
                self.create_metadata_key(key)

    def fetch_metadata_values(self, metadata_id):
        """Fetch metadata values for a given metadata key ID"""
        response = self.session.get(
            f"{self.base_url}/account-service/api/vectordb/metadata/value?size=50&metadataId={metadata_id}"
        )
        if response.status_code == 200:
            data = response.json()
            return {item["metadataValue"] for item in data.get("content", [])}
        else:
            raise Exception(f"Failed to fetch metadata values: {response.text}")

    def create_metadata_value(self, metadata_id, metadata_value):
        """Create a new metadata value"""
        response = self.session.post(
            f"{self.base_url}/account-service/api/vectordb/metadata/value",
            json={"metadataId": metadata_id, "metadataValue": metadata_value}
        )
        if response.status_code != 201:
            raise Exception(f"Failed to create metadata value {metadata_value}: {response.text}")

    def ensure_metadata_values_exist(self, required_metadata):
        """Ensure all required metadata values exist for each key"""
        for key, values in required_metadata.items():
            metadata_id = self.existing_metadata.get(key)
            if metadata_id:
                existing_values = self.fetch_metadata_values(metadata_id)
                for value in values:
                    if value not in existing_values:
                        self.create_metadata_value(metadata_id, value)

    def ensure_metadata(self, required_metadata):
        """Ensure all metadata keys and values exist"""
        self.ensure_metadata_keys_exist(required_metadata)
        self.ensure_metadata_values_exist(required_metadata)
        print("Metadata keys and values are synchronized.")

    def fetch_vector_dbs(self):
        """Fetch all vector DBs and store relevant details"""
        response = self.session.get(
            f"{self.base_url}/governance-service/api/ai/vectordb?size=100&sort=createTime,desc"
        )
        if response.status_code == 200:
            data = response.json()
            self.existing_vectordbs = {
                item["name"]: {
                    "id": item["id"],
                    "type": item["type"],
                    "userEnforcement": item["userEnforcement"],
                    "groupEnforcement": item["groupEnforcement"]
                }
                for item in data.get("content", [])
            }
        else:
            raise Exception(f"Failed to fetch vector DBs: {response.text}")

    def create_vector_db(self, db_data):
        """Create a new vector DB"""
        response = self.session.post(
            f"{self.base_url}/governance-service/api/ai/vectordb",
            json={**db_data, "status": 1, "description": ""}
        )
        if response.status_code != 201:
            raise Exception(f"Failed to create vector DB {db_data['name']}: {response.text}")

    def update_vector_db(self, db_id, db_data):
        """Update an existing vector DB"""
        response = self.session.put(
            f"{self.base_url}/governance-service/api/ai/vectordb/{db_id}",
            json={**db_data, "id": db_id, "status": 1, "description": ""}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to update vector DB {db_data['name']}: {response.text}")

    def ensure_vector_dbs(self, required_vector_dbs):
        """Ensure all required vector DBs exist and match the expected settings"""
        self.fetch_vector_dbs()

        for required_db in required_vector_dbs:
            name = required_db["name"]
            if name in self.existing_vectordbs:
                existing_db = self.existing_vectordbs[name]
                if (
                        existing_db["type"] != required_db["type"] or
                        existing_db["userEnforcement"] != required_db["userEnforcement"] or
                        existing_db["groupEnforcement"] != required_db["groupEnforcement"]
                ):
                    print(f"Updating vector DB: {name}")
                    self.update_vector_db(existing_db["id"], required_db)
                else:
                    print(f"Vector DB {name} is already up to date.")
            else:
                print(f"Creating new vector DB: {name}")
                self.create_vector_db(required_db)

        print("Vector DB synchronization complete.")

    def fetch_ai_applications(self):
        """Fetch the list of AI applications."""
        url = f"{self.base_url}/governance-service/api/ai/application?size=100&sort=createTime,desc"
        response = self.session.get(url, verify=False)
        if response.status_code == 200:
            return response.json().get("content", [])
        else:
            print(f"Failed to fetch applications: {response.status_code}")
            return []

    def create_ai_application(self, app: dict):
        """Create a new AI application."""
        url = f"{self.base_url}/governance-service/api/ai/application"
        app_name = app["name"]
        payload = {
            "name": app_name,
            "applicationKey": "",
            "description": app["description"],
            "status": 1,
            "deploymentType": "CLOUD",
            "vectorDBs": app["vectorDBs"],
            "guardrailDetails": app.get("guardrailDetails", ""),
            "tenantId": 1
        }
        response = self.session.post(url, json=payload, verify=False)
        if response.status_code == 201:
            print(f"Application '{app_name}' created successfully.")
            return response.json()
        else:
            print(f"Failed to create '{app_name}': {response.status_code} - {response.text}")
            return None

    def ensure_ai_applications(self, required_apps):
        """Ensure 'Plant Operations' and 'Plant Operations Unsafe' exist."""
        existing_apps = self.fetch_ai_applications()
        existing_app_names = {app["name"] for app in existing_apps}

        current_apps = {app["name"]: app for app in existing_apps}

        for app in required_apps:
            if app["name"] not in existing_app_names:
                ai_app = self.create_ai_application(app)
                if ai_app:
                    current_apps[app["name"]] = ai_app
            else:
                print(f"Application '{app['name']}' already exists.")

            current_app = current_apps[app["name"]]
            if "config" in app:
                self.update_ai_app_config(current_app["id"], app["config"])

            if "policies" in app:
                self.update_ai_app_policies(current_app["id"], app["policies"])

    def update_ai_app_config(self, ai_app_id, config):
        """Update AI application configuration."""
        response = self.session.put(f"{self.base_url}/governance-service/api/ai/application/{ai_app_id}/config", json=config, verify=False)
        if response.status_code == 200:
            print(f"AI app config updated successfully.")
        else:
            print(f"Failed to update AI app config: {response.status_code}, {response.text}")

    def update_ai_app_policies(self, ai_app_id, policies):
        """Update AI application policies."""

        # List all policies descriptions
        policy_descriptions = [policy["description"] for policy in policies]

        # Fetch all policies
        existing_policies_response = self.session.get(f"{self.base_url}/governance-service/api/ai/application/{ai_app_id}/policy?size=100", verify=False)
        if existing_policies_response.status_code == 200:
            existing_policies = existing_policies_response.json().get("content", [])

            # Disable all existing policies
            for existing_policy in existing_policies:
                policy_id = existing_policy.get("id")
                if existing_policy["status"] != 0:
                    response = self.session.put(f"{self.base_url}/governance-service/api/ai/application/{ai_app_id}/policy/{policy_id}", json=existing_policy, verify=False)
                    if response.status_code == 200:
                        print(f"Policy {policy_id} disabled successfully.")
                    else:
                        print(f"Failed to disable policy {policy_id}: {response.status_code}, {response.text}")
        else:
            print(f"Failed to fetch existing policies: {existing_policies_response.status_code}, {existing_policies_response.text}")
            return

        # Get the policy by description
        for policy in policies:
            policy_description = policy["description"]

            # Get the policy by description from existing policies
            existing_policy = next((p for p in existing_policies if p["description"] == policy_description), None)

            # If the policy exists, update it
            if existing_policy:
                policy_id = existing_policy.get("id")
                policy["id"] = policy_id
                response = self.session.put(f"{self.base_url}/governance-service/api/ai/application/{ai_app_id}/policy/{policy_id}", json=policy, verify=False)

                if response.status_code == 200:
                    print(f"AI app policy updated successfully.")
                else:
                    print(f"Failed to update AI app policy: {response.status_code}, {response.text}")
            else:
                # Create a new policy
                response = self.session.post(f"{self.base_url}/governance-service/api/ai/application/{ai_app_id}/policy", json=policy, verify=False)

                if response.status_code == 201:
                    print(f"AI app policy created successfully.")
                else:
                    print(f"Failed to create AI app policy: {response.status_code}, {response.text}")

    def fetch_eval_target_applications(self):
        """Fetch the list of Eval target applications."""
        url = f"{self.base_url}/eval-service/api/target/application/list?size=100&sort=createTime,desc"
        response = self.session.get(url, verify=False)
        if response.status_code == 200:
            return response.json().get("content", [])
        else:
            print(f"Failed to fetch eval target applications: {response.status_code}")
            return []

    def ensure_eval_target_applications(self, eval_target_apps):
        existing_ai_apps = self.fetch_ai_applications()
        existing_eval_target_apps = self.fetch_eval_target_applications()

        existing_ai_app_name_ids = {app["name"]:app["id"] for app in existing_ai_apps}
        existing_eval_target_app_name_ids = {app["name"]:app["target_id"] for app in existing_eval_target_apps}

        for eval_target_app in eval_target_apps:
            if eval_target_app["name"] in existing_eval_target_app_name_ids:
                eval_target_app["id"] = existing_eval_target_app_name_ids[eval_target_app["name"]]

            if eval_target_app["name"] in existing_ai_app_name_ids:
                eval_target_app["ai_application_id"] = existing_ai_app_name_ids[eval_target_app["name"]]

            if "id" in eval_target_app and eval_target_app["id"]:
                eval_target_app_id = eval_target_app["id"]
                response = self.session.put(f"{self.base_url}/eval-service/api/target/application/{eval_target_app_id}", json=eval_target_app, verify=False)
                if response.status_code == 200:
                    print(f"Eval target application '{eval_target_app['name']}' updated successfully.")
                else:
                    print(f"Failed to update eval target application '{eval_target_app['name']}': {response.status_code}, {response.text}")
            else:
                response = self.session.post(f"{self.base_url}/eval-service/api/target/application", json=eval_target_app, verify=False)
                if response.status_code == 200:
                    print(f"Eval target application '{eval_target_app['name']}' created successfully.")
                else:
                    print(f"Failed to create eval target application '{eval_target_app['name']}': {response.status_code}, {response.text}")

    def ensure_eval_users_exist_in_securechat(self, securechat_server_base_urls, required_users):
        """Ensure expected users exist with the correct groups."""
        for securechat_server_base_url in securechat_server_base_urls:
            for user in required_users:
                payload = {
                    "user_name": user
                }
                response = self.session.post(f"{securechat_server_base_url}//securechat/api/v1/user/login", json=payload, verify=False)
                if response.status_code == 200:
                    print(f"Securechat User '{user}' created successfully.")
                else:
                    print(f"Failed to create securechat user '{user}':", response.text)

if __name__ == "__main__":
    BASE_URL = "http://localhost:4545"
    USERNAME = "admin"
    PASSWORD = "welcome1"
    REQUIRED_GROUPS = [
        "plant_managers",
        "plant_managers_be_de",
        "plant_managers_tx_us",
        "plant_operators_tx_us",
        "plant_operators_be_de",
        "plant_operators"
    ]

    REQUIRED_USERS = {
        "marta": ["plant_managers_be_de", "plant_managers"],
        "michael": ["plant_operators_be_de", "plant_operators"],
        "rick": ["plant_managers_tx_us", "plant_managers"],
        "kate": ["plant_operators_tx_us", "plant_operators"],
        "martha": ["plant_managers_be_de", "plant_managers"],
        "sally": []
    }

    REQUIRED_METADATA = {
        "SECURITY": ["CONFIDENTIAL", "RESTRICTED", "INTERNAL", "PUBLIC"],
        "GDPR_CONTENT": ["YES", "NO"],
        "ADVERTISEMENT_CONSENT": ["TRUE", "FALSE"]
    }

    REQUIRED_VECTOR_DBS = [
        {
            "name": "Plant Operations Vector DB",
            "type": "OPENSEARCH",
            "userEnforcement": 1,
            "groupEnforcement": 1,
        },
        {
            "name": "Sales Intel Vector DB",
            "type": "OPENSEARCH",
            "userEnforcement": 0,
            "groupEnforcement": 0,
        },
        {
            "name": "IT Support Vector DB",
            "type": "OPENSEARCH",
            "userEnforcement": 1,
            "groupEnforcement": 1,
        },
    ]

    REQUIRED_AI_APPS = [
        {
            "name": "Plant Operations - Safe",
            "description": "Assistant for Plant Operations. This helps Plant Operators to troubleshoot common issues. It also helps Plant Managers to check inventories.",
            "vectorDBs": ["Plant Operations Vector DB"],
            "guardrailDetails": "{\"guardrail_enable\":true,\"guardrail_id\":\"uy4svg62jlan\",\"guardrail_version\":\"DRAFT\",\"region\":\"us-east-1\"}",
            "config": {
                "allowedUsers": [],
                "allowedGroups": [
                    "plant_managers",
                    "plant_operators"
                ],
                "allowedRoles": [],
                "deniedUsers": [],
                "deniedGroups": [],
                "deniedRoles": [],
            },
            "policies": [
                {
                    "status": 1,
                    "description": "Highly Sensitive Information Blocking",
                    "users": [],
                    "groups": [
                        "public"
                    ],
                    "roles": [],
                    "tags": [
                        "US_SSN",
                        "CREDIT_CARD"
                    ],
                    "prompt": "DENY",
                    "reply": "DENY",
                    "enrichedPrompt": "DENY",
                },
                {
                    "status": 1,
                    "description": "Toxic Content Blocking",
                    "users": [],
                    "groups": [
                        "public"
                    ],
                    "roles": [],
                    "tags": [
                        "TOXIC"
                    ],
                    "prompt": "DENY",
                    "reply": "DENY",
                    "enrichedPrompt": "DENY"
                },
                {
                    "status": 1,
                    "description": "Personal Identifier Redaction",
                    "users": [],
                    "groups": [
                        "public"
                    ],
                    "roles": [],
                    "tags": [
                        "EMAIL_ADDRESS",
                        "PHONE_NUMBER",
                        "PERSON"
                    ],
                    "prompt": "DENY",
                    "reply": "REDACT",
                    "enrichedPrompt": "ALLOW"
                }
            ]
        },
        {
            "name": "Plant Operations - Unsafe",
            "description": "Assistant for Plant Operations. This helps Plant Operators to troubleshoot common issues. It also helps Plant Managers to check inventories.",
            "vectorDBs": [],
        },
        {
            "name": "Sales Intel - Safe",
            "description": "",
            "vectorDBs": [],
        },
        {
            "name": "Sales Intel - Unsafe",
            "description": "",
            "vectorDBs": [],
        },
        {
            "name": "IT Support - Safe",
            "description": "",
            "vectorDBs": ["IT Support Vector DB"],
        },
        {
            "name": "IT Support - Unsafe",
            "description": "",
            "vectorDBs": ["IT Support Vector DB"],
        }
    ]

    EVAL_TARGET_APPLICATIONS = [
        {
            "name": "Sales Intel - Safe",
            "connectionType": "HTTP/HTTPS-Endpoint",
            "url": f"http://paig-securechat-safe-container:5555/securechat/api/v1/conversations/prompt",
            "headers": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhbGx5In0.X5WgFihYGovrvlS4D4UILpl3XGNfgC3AKbh_jdPWGnY"},
            "body": "{\n  \"ai_application_name\": \"sales_model\",\n  \"prompt\": \"{{prompt}}\"\n}",
            "transformResponse": "json.messages && json.messages.length > 0 \n  ? (json.messages.find(message => message.type === 'reply') || {}).content || \"No reply found.\"\n  : \"No response from the server.\"",
            "method": "POST"
        },
        {
            "name": "Sales Intel - Unsafe",
            "connectionType": "HTTP/HTTPS-Endpoint",
            "url": f"http://paig-securechat-unsafe-container:6565/securechat/api/v1/conversations/prompt",
            "headers": {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhbGx5In0.X5WgFihYGovrvlS4D4UILpl3XGNfgC3AKbh_jdPWGnY"},
            "body": "{\n  \"ai_application_name\": \"sales_model\",\n  \"prompt\": \"{{prompt}}\"\n}",
            "transformResponse": "json.messages && json.messages.length > 0 \n  ? (json.messages.find(message => message.type === 'reply') || {}).content || \"No reply found.\"\n  : \"No response from the server.\"",
            "method": "POST"
        }
    ]

    client = DemoDataClient(BASE_URL, USERNAME, PASSWORD)
    client.ensure_groups_exist(REQUIRED_GROUPS)
    client.ensure_users_exist(REQUIRED_USERS)
    client.ensure_metadata(REQUIRED_METADATA)
    client.ensure_vector_dbs(REQUIRED_VECTOR_DBS)
    client.ensure_ai_applications(REQUIRED_AI_APPS)
    client.ensure_eval_target_applications(EVAL_TARGET_APPLICATIONS)
    client.ensure_eval_users_exist_in_securechat(["http://paig-securechat-safe-container:5555", "http://paig-securechat-unsafe-container:6565"], ["sally"])