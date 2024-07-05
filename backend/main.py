import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

load_dotenv()

medium_api_key = os.getenv("MEDIUM_API_KEY")
medium_base_url = os.getenv("MEDIUM_API_BASE_URL")
hashnode_api_key = os.getenv("HASHNODE_API_KEY")
hashnode_base_url = os.getenv("HASHNODE_API_BASE_URL")
devto_api_key = os.getenv("DEVTO_API_KEY")
devto_base_url = os.getenv("DEVTO_API_BASE_URL")

def authenticate_user(username, password):
    # Simple authentication simulation
    users = {
        "user1": "password1",
        "user2": "password2",
    }
    return users.get(username) == password

def post_to_medium(title, content):
    headers = {
        "Authorization": f"Bearer {medium_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "title": title,
        "contentFormat": "html",
        "content": content,
        "publishStatus": "public",
    }

    response = requests.post(f"{medium_base_url}/posts", json=data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": response.text}

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

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def post_to_devto(title, content):
    headers = {
        "Authorization": f"Bearer {devto_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "title": title,
        "body_markdown": content,
        "tags": [],
        "published": True,
    }

    response = requests.post(f"{devto_base_url}/articles", json=data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": response.text}

def save_draft(title, content):
    draft = {
        "title": title,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    with open("drafts.json", "a") as f:
        json.dump(draft, f)
        f.write("\n")
    return {"status": "Draft saved"}

def schedule_post(title, content, schedule_time):
    delay = (schedule_time - datetime.now()).total_seconds()
    if delay > 0:
        time.sleep(delay)
    post_to_all(title, content)
    return {"status": "Post scheduled"}

def post_to_all(title, content):
    medium_response = post_to_medium(title, content)
    print("Medium Response:", medium_response)

    hashnode_response = post_to_hashnode(title, content)
    print("Hashnode Response:", hashnode_response)

    devto_response = post_to_devto(title, content)
    print("Dev.to Response:", devto_response)

def main():
    username = input("Username: ")
    password = input("Password: ")

    if not authenticate_user(username, password):
        print("Authentication failed")
        return

    print("1. Post now")
    print("2. Save draft")
    print("3. Schedule post")
    choice = input("Choose an option: ")

    title = input("Title: ")
    content = input("Content (HTML format): ")

    if choice == "1":
        post_to_all(title, content)
    elif choice == "2":
        save_draft(title, content)
    elif choice == "3":
        schedule_time_str = input("Schedule time (YYYY-MM-DD HH:MM:SS): ")
        schedule_time = datetime.strptime(schedule_time_str, "%Y-%m-%d %H:%M:%S")
        schedule_post(title, content, schedule_time)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
