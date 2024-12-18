import json

import requests
import threading

# Globals and Lock for shared cookies
GLOBAL_COOKIES = {}
COOKIE_LOCK = threading.Lock()


def get_auth_cookies(securechat_base_url, payload):
    """
    Logs in to the server and retrieves cookies for authentication.

    Args:
        securechat_base_url (str): Base URL of the endpoint you want to call.
        payload (dict): Dictionary containing login credentials (e.g., username and password).

    Returns:
        dict: Authentication cookies.
    """
    headers = {
        'Content-Type': 'application/json'
    }

    login_url = securechat_base_url + "/securechat/api/v1/user/login"
    response = requests.post(login_url, headers=headers, data=json.dumps(payload), timeout=120)
    if response.status_code == 200:
        return response.cookies.get_dict()
    else:
        raise Exception(f"Login failed with status code {response.status_code}: {response.text}")


def get_or_set_global_cookies(securechat_base_url, username):
    """
    Checks if cookies for a specific URL and user are already set; logs in and sets them if not.

    Args:
        securechat_base_url (str): Base URL of the endpoint you want to call.
        username (str): Username for which to fetch cookies.

    Returns:
        dict: Authentication cookies.
    """
    global GLOBAL_COOKIES
    user_key = (securechat_base_url, username)  # Tuple as unique key for URL-user pair

    # Ensure thread-safe access with a lock
    with COOKIE_LOCK:
        if user_key not in GLOBAL_COOKIES:
            # Fetch cookies and store them globally
            credentials = {"user_name": username}
            GLOBAL_COOKIES[user_key] = get_auth_cookies(securechat_base_url, credentials)

    return GLOBAL_COOKIES[user_key]


def make_authenticated_request(securechat_base_url, username, payload=None):
    """
    Makes an authenticated request using cookies specific to URL and user.

    Args:
        securechat_base_url (str): Base URL of the endpoint you want to call.
        username (str): Username for authentication.
        payload (dict): Request payload for the API (optional).

    Returns:
        dict: Response data from the authenticated request.
    """
    cookies = get_or_set_global_cookies(securechat_base_url, username)

    headers = {
        "Content-Type": "application/json"
    }

    prompt_url = securechat_base_url + "/securechat/api/v1/conversations/prompt"
    response = requests.post(prompt_url, json=payload, cookies=cookies, headers=headers, timeout=120)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")


def call_api(prompt, options, context):
    """
    Main function to handle API calls with cookies managed for multiple users and URLs.

    Args:
        prompt (str): User's prompt.
        options (dict): Configuration options including base URL, username, and AI app name.
        context (dict): Additional context for the call.

    Returns:
        dict: Response output from the API.
    """
    # Get config values
    securechat_base_url = options.get("config").get("base_url")
    securechat_user = options.get("config").get("username")
    ai_application_name = options.get("config").get("ai_application_name")
    max_retry_attempts = int(options.get("config").get("max_retry_attempts"))

    print(f"securechat_base_url: {securechat_base_url}")
    print(f"securechat_user: {securechat_user}")
    print(f"ai_application_name: {ai_application_name}")
    print(f"prompt: {prompt}")

    request_data = {
        "prompt": prompt,
        "ai_application_name": ai_application_name
    }

    # Retry request with max_retry_attempts
    response = None
    error_message = None
    for _ in range(max_retry_attempts):
        try:
            response = make_authenticated_request(securechat_base_url, securechat_user, request_data)
            break
        except Exception as e:
            error_message = str(e)
            response = None

    if response is not None:
        if "messages" in response and len(response["messages"]) > 1:
            return {"output": response["messages"][1]["content"]}
        elif type(response) == list and len(response) > 1:
            return {"output": response[1]["content"]}
        else:
            return {"error": "No response from the server."}
    else:
        return {"error": error_message}

