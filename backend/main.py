import requests
import os
from dotenv import load_dotenv

load_dotenv()

medium_api_key = os.getenv("MEDIUM_API_KEY")
medium_base_url = os.getenv("MEDIUM_API_BASE_URL")
hashnode_api_key = os.getenv("HASHNODE_API_KEY")
hashnode_base_url = os.getenv("HASHNODE_API_BASE_URL")
devto_api_key = os.getenv("DEVTO_API_KEY")
devto_base_url = os.getenv("DEVTO_API_BASE_URL")


def post_to_medium(title, content):
    headers = {
        "Authorization": f"Bearer {medium_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "title": title,
        "content-format": "html",
        "content": content,
        "publishStatus": "public",
    }

    response = requests.post(f"{medium_base_url}/users/@me/posts", json=data, headers=headers)
    return response.json()

def post_to_hashnode(title, content):
    headers = {
        "Authorization": f"Bearer {hashnode_api_key}",
        "Content-Type": "application/json",
    }

    query = """
        mutation CreatePost($title: String!, $content: String!, $tags: [String!]!) {
            createPublicationStory(input: {
                title: $title,
                contentMarkdown: $content,
                tags: $tags
            }) {
                code
                message
                success
                post {
                    slug
                    title
                }
            }
        }
    """

    variables = {
        "title": title,
        "content": content,
        "tags": [],
    }

    response = requests.post(
        hashnode_base_url,
        json={"query": query, "variables": variables},
        headers=headers
    )

    return response.json()

def post_to_devto(title, content):
    headers = {
        "Authorization": f"Bearer {devto_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "title": title,
        "body_markdown": content,
        "tags": "",
        "published": True,
    }

    response = requests.post(f"{devto_base_url}/users/@me/posts", json=data, headers=headers)
    return response.json()

def main():
    title = "Your article Title"
    content = "<p>Your article content in HTML format</p>"

    # Post to Medium
    medium_response = post_to_medium(title, content)
    print("Medium Response:", medium_response)

    # Post to Hashnode
    hashnode_response = post_to_hashnode(title, content)
    print("Hashnode Response:", hashnode_response)

    # Post to dev.to
    devto_response = post_to_devto(title, content)
    print("Dev.to Response:", devto_response)

if __name__ == "__main__":
    main()