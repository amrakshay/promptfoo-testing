import json
import os
from opensearchpy import OpenSearch
import boto3
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

document_folder="documents"
meta_file_path = os.path.join(document_folder, "meta.json")

index_name = os.getenv("INDEX_NAME")
print(f"INDEX_NAME={index_name}")

# Initialize OpenSearch client
opensearch_client = OpenSearch(
    hosts=[{'host': os.getenv("OS_HOST"), 'port': int(os.getenv("OS_PORT"))}],
    http_auth=(os.getenv("OS_USERNAME"), os.getenv("OS_PASSWORD")),
    use_ssl=True,
    verify_certs=False
)

client_kwargs = {}
if os.getenv('AWS_REGION'):
    client_kwargs['region_name'] = os.getenv('AWS_REGION')

region = os.getenv('AWS_REGION')
if not region or region == '':
    client_kwargs['region'] = 'us-east-1'
else:
    client_kwargs['region'] = region

print(f"Using AWS_REGION={os.getenv('AWS_REGION')}")

if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY') != '':
    client_kwargs['aws_access_key_id'] = os.getenv('AWS_ACCESS_KEY_ID')

if os.getenv('AWS_SECRET_ACCESS_KEY') and os.getenv('AWS_SECRET_ACCESS_KEY') != '':
    client_kwargs['aws_secret_access_key'] = os.getenv('AWS_SECRET_ACCESS_KEY')

if os.getenv('AWS_SESSION_TOKEN') and os.getenv('AWS_SESSION_TOKEN') != '':
    client_kwargs['aws_session_token'] = os.getenv('AWS_SESSION_TOKEN')

print(f"client_kwargs={client_kwargs}")

REQUIRED_ACCESS_KEYS = ['aws_access_key_id', 'aws_secret_access_key']
REQUIRED_SESSION_KEYS = ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']

def create_bedrock_client(client_name: str, connection_details: dict):
    """Create a Boto3 client for the Bedrock service based on the provided credentials.

    Returns:
        boto3.client: A Boto3 client for the Bedrock service.
    """
    if all(key in connection_details for key in REQUIRED_SESSION_KEYS):
        return boto3.client(
            client_name,
            aws_access_key_id=connection_details['aws_access_key_id'],
            aws_secret_access_key=connection_details['aws_secret_access_key'],
            aws_session_token=connection_details['aws_session_token'],
            region_name=connection_details['region']
        )

    if all(key in connection_details for key in REQUIRED_ACCESS_KEYS):
        return boto3.client(
            client_name,
            aws_access_key_id=connection_details['aws_access_key_id'],
            aws_secret_access_key=connection_details['aws_secret_access_key'],
            region_name=connection_details['region']
        )

    return boto3.client(client_name, region_name=connection_details['region'])

# Initialize Bedrock client for embedding generation
bedrock_client = create_bedrock_client("bedrock-runtime", client_kwargs)

def generate_embedding(text):
    """
    Generates an embedding for the given text using AWS Bedrock.

    :param text: The text to generate an embedding for.
    :return: The embedding vector for the text.
    """
    payload = {"inputText": f"{text}"}
    body = json.dumps(payload)
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_client.invoke_model(
        body=body, modelId=os.getenv("BEDROCK_EMBEDDING_MODEL"), accept=accept, contentType=contentType
    )
    print(response)
    response_body = json.loads(response.get("body").read())
    print(response_body)

    embedding = response_body.get("embedding")

    return embedding


def get_collection_data():
    """
    Reads the customer support tickets data from a JSON file and prepares the data for indexing.

    :return: A list of records ready to be indexed in OpenSearch.
    """
    records = []

    # Read json file using json
    with open(meta_file_path) as articles_details_file:
        document_details = json.load(articles_details_file)

        for document_entry in document_details:
            source = document_entry['source']

            # Read the source text from the file
            with open(source) as articles_file:
                all_articles_text = articles_file.read()

                # Split the articles by '---'
                articles = all_articles_text.split("---")

                for article in articles:
                    article = article.strip()
                    if article == "":
                        continue

                    # Generate the embedding for the article
                    vector = generate_embedding(article)

                    # Prepare the record
                    record = {
                        "_index": index_name,
                        "_source": {
                            "vector_field": vector,
                            "text": article,
                            "metadata": {
                                "source": source
                            }
                        }
                    }
                    # Groups are given, then
                    if "groups" in document_entry:
                        record["_source"]["metadata"]["groups"] = document_entry["groups"]
                    if "users" in document_entry:
                        record["_source"]["metadata"]["users"] = document_entry["users"]

                    records.append(record)

    return records


def create_index():
    """
    Creates an OpenSearch index with a mapping for storing articles and embeddings.
    """
    index_body = {
        "mappings": {
            "properties": {
                "vector_field": {
                    "type": "knn_vector",
                    "dimension": 1536
                },
                "text": {"type": "text"},
                "metadata": {
                    "properties": {
                        "source": {"type": "text"},
                        "users": {"type": "text"},
                        "groups": {"type": "text"},
                        "metadata": {"type": "object"}
                    }
                }
            }
        },
        "settings": {
            "index": {
                "knn": True,
                "knn.space_type": "cosinesimil"
            }
        }
    }

    # Create index if it doesn't exist
    if opensearch_client.indices.exists(index=index_name):
        opensearch_client.indices.delete(index=index_name)

    if not opensearch_client.indices.exists(index=index_name):
        opensearch_client.indices.create(index=index_name, body=index_body)
        print("OpenSearch index created successfully.")
    else:
        print("Index already exists.")


def insert_data(data):
    """
    Inserts the given data into the OpenSearch index.

    :param data: The list of records to insert into the index.
    """
    bulk_data = []
    for record in data:
        bulk_data.append({"index": {"_index": index_name}})
        bulk_data.append(record["_source"])

    # Bulk insert data into OpenSearch
    response = opensearch_client.bulk(body=bulk_data)
    if response["errors"]:
        print(f"Error inserting data into OpenSearch. {response}")
    else:
        print("Data inserted successfully into OpenSearch.")


# Create OpenSearch index
create_index()

# Get the collection data
collection_data = get_collection_data()
print(collection_data)

# Insert data into OpenSearch
insert_data(collection_data)
