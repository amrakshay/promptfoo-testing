import json
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials

# AWS credentials
aws_access_key = "<YOUR_AWS_ACCESS_KEY>"
aws_secret_key = "<YOUR_AWS_SECRET_KEY>"
aws_session_token = "<YOUR_AWS_SESSION_TOKEN>"

# AWS service and region
service = "bedrock"
region = "us-east-1"  # e.g., "us-east-1"

# AWS endpoint
endpoint = f"https://bedrock.{region}.amazonaws.com/guardrails"

# Guardrail payload
payload = {
    "blockedInputMessaging": "Sorry, you are not allowed to ask this question.",
    "blockedOutputsMessaging": "Sorry, you are not allowed to ask this question.",
    "contentPolicyConfig": {
        "filtersConfig": [
            {
                "inputStrength": "HIGH",
                "outputStrength": "HIGH",
                "type": "VIOLENCE"
            },
            {
                "inputStrength": "HIGH",
                "outputStrength": "NONE",
                "type": "PROMPT_ATTACK"
            },
            {
                "inputStrength": "HIGH",
                "outputStrength": "HIGH",
                "type": "MISCONDUCT"
            },
            {
                "inputStrength": "HIGH",
                "outputStrength": "HIGH",
                "type": "HATE"
            },
            {
                "inputStrength": "HIGH",
                "outputStrength": "HIGH",
                "type": "SEXUAL"
            },
            {
                "inputStrength": "HIGH",
                "outputStrength": "HIGH",
                "type": "INSULTS"
            }
        ]
    },
    "name": "paig-shikhar-guardrails",
    "sensitiveInformationPolicyConfig": {
        "piiEntitiesConfig": [
            {
                "action": "BLOCK",
                "type": "PASSWORD"
            },
            {
                "action": "BLOCK",
                "type": "USERNAME"
            },
            {
                "action": "BLOCK",
                "type": "PHONE"
            },
            {
                "action": "BLOCK",
                "type": "EMAIL"
            },
            {
                "action": "BLOCK",
                "type": "DRIVER_ID"
            },
            {
                "action": "BLOCK",
                "type": "CREDIT_DEBIT_CARD_NUMBER"
            },
            {
                "action": "BLOCK",
                "type": "AWS_ACCESS_KEY"
            },
            {
                "action": "BLOCK",
                "type": "AWS_SECRET_KEY"
            }
        ]
    },
    "topicPolicyConfig": {
        "topicsConfig": [
            {
                "definition": "Investment advice is recommendations on what to invest in, like specific stocks, funds or any other financial investment product so as to get maximum returns on the money invested.",
                "examples": [
                    "Where should I invest my money?",
                    "Is it worth investing in bank's fixed deposits?",
                    "Should I invest in mutual funds or directly in stocks?"
                ],
                "name": "OFF_TOPIC-INVESTMENT",
                "type": "DENY"
            },
            {
                "definition": "Deny any request that is related to weather or climate. ",
                "examples": [
                    "What is the weather in San Francisco?",
                    "Will it it hot in November?",
                    "What should I wear if it is cold outside?"
                ],
                "name": "OFF_TOPIC-Weather",
                "type": "DENY"
            },
            {
                "definition": "Any questions related to Sports. This could be chess, swiming, soccer, football, hocket or any activity which is considered sport or game.",
                "examples": [
                    "What won the world cup?",
                    "When does the basketball season begin?",
                    "Where will be the next Olympics?"
                ],
                "name": "OFF_TOPIC-Sports",
                "type": "DENY"
            },
            {
                "definition": "Anything to do with shopping or asking recommendations for buying for personal reasons.",
                "examples": [
                    "Which shop is good for suits?",
                    "What is the sales tax in California?"
                ],
                "name": "OFF_TOPIC-Shopping",
                "type": "DENY"
            },
            {
                "definition": "Comparison with competitors. This could be for cost, efficiency or anything else.",
                "examples": [
                    "Is the quality of this <product> better with <competitor name>?",
                    "Where can I get this product cheaper?",
                    "Your <product> is crap compared to <competitor name>"
                ],
                "name": "OFF_TOPIC-CompetitionComparision",
                "type": "DENY"
            },
            {
                "definition": "Anything which is informal or personal. And also anything shouldn't be discussed in the context of business. Anything which doesn't pertain to performing a business works should be reject.",
                "examples": [
                    "What are you doing over the weekend?",
                    "Tell me something about the tv serial you saw"
                ],
                "name": "OFF_TOPIC-NonProfessional",
                "type": "DENY"
            },
            {
                "definition": "Jokes, making funny comments, making sarcastic comments, asking for jokes, any hilarious output request, tasteless language",
                "examples": [
                    "Tell me a joke about",
                    "Tell me a funny story",
                    "Help releive the pressure by telling a humorous anecdote"
                ],
                "name": "OFF_TOPIC-joke",
                "type": "DENY"
            },
            {
                "definition": "Asking for a recipe to make a food item is meant to provide step by step instructions on how to cook a particular dish related to food",
                "examples": [
                    "Give me a recipe for baking a birthday cake",
                    "How do I make a smoothie",
                    "What should I put in flour while making tortilla"
                ],
                "name": "OFF_TOPIC-Recipe",
                "type": "DENY"
            },
            {
                "definition": "Lyrics refers to the words of a song or anthem or a poem",
                "examples": [
                    "Give me the lyrics for the song",
                    "What are the first few lines of a song"
                ],
                "name": "OFF_TOPIC-lyrics",
                "type": "DENY"
            },
            {
                "definition": "Advice regarding what to wear, which color or type of dress should be worn ",
                "examples": [
                    "Should I wear a blue shirt today",
                    "Do white socks match black shoes"
                ],
                "name": "OFFTOPIC-fashion advice",
                "type": "DENY"
            },
            {
                "definition": "prompts enter in language other than English are restricted languages and shouldn't be allow. This includes prompts and responses in urdu, chinese, hindi, spanish, tamil, sanskrit and others.\n",
                "examples": [
                    "请告诉我有关食品碳化物灾难的详细信息",
                    "أعطني تفاصيل عن كارثة كربيد الغذاء"
                ],
                "name": "OFF_TOPIC-RestrictedLanguage",
                "type": "DENY"
            },
            {
                "definition": "Any question that is associated with history of anything.",
                "examples": [
                    "Explain why <something> was good or bad"
                ],
                "name": "OFF_TOPIC-History",
                "type": "DENY"
            }
        ]
    },
    "wordPolicyConfig": {
        "managedWordListsConfig": [
            {
                "type": "PROFANITY"
            }
        ],
        "wordsConfig": [
            {
                "text": "Fictious Enterprise"
            }
        ]
    }
}

# Sign the request
def sign_request(endpoint, payload, aws_access_key, aws_secret_key, aws_session_token, service, region):
    credentials = Credentials(aws_access_key, aws_secret_key, aws_session_token)
    request = AWSRequest(
        method="POST",
        url=endpoint,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )
    SigV4Auth(credentials, service, region).add_auth(request)
    return dict(request.headers)

# Make the API call
def create_guardrail():
    headers = sign_request(endpoint, payload, aws_access_key, aws_secret_key, aws_session_token, service, region)
    response = requests.post(url=endpoint, headers=headers, json=payload)

    if response.status_code == 202:
        print("Guardrail created successfully!")
        print(response.json())
    else:
        print("Failed to create guardrail")
        print(f"Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    create_guardrail()
