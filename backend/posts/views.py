from django.shortcuts import render
import threading
import requests
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import Post, Draft
from .serializers import PostSerializer, DraftSerializer

medium_api_key = os.getenv("MEDIUM_API_KEY")
medium_base_url = os.getenv("MEDIUM_API_BASE_URL")
hashnode_api_key = os.getenv("HASHNODE_API_KEY")
hashnode_base_url = os.getenv("HASHNODE_API_BASE_URL")
devto_api_key = os.getenv("DEVTO_API_KEY")
devto_base_url = os.getenv("DEVTO_API_BASE_URL")

@api_view(['GET'])
def list_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

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

def post_to_all(title, content):
    medium_response = post_to_medium(title, content)
    hashnode_response = post_to_hashnode(title, content)
    devto_response = post_to_devto(title, content)
    return {
        "medium": medium_response,
        "hashnode": hashnode_response,
        "devto": devto_response,
    }

@api_view(['POST'])
def post_content(request):
    title = request.data.get('title')
    content = request.data.get('content')
    platform = request.data.get('platform')
    if platform == "medium":
        response = post_to_medium(title, content)
    elif platform == "hashnode":
        response = post_to_hashnode(title, content)
    elif platform == "devto":
        response = post_to_devto(title, content)
    else:
        response = {"error": "Invalid platform"}
    return Response(response)

@api_view(['POST'])
def save_draft(request):
    title = request.data.get('title')
    content = request.data.get('content')
    draft = Draft.objects.create(title=title, content=content)
    serializer = DraftSerializer(draft)
    return Response(serializer.data)

@api_view(['POST'])
def schedule_post(request):
    title = request.data.get('title')
    content = request.data.get('content')
    schedule_time_str = request.data.get('schedule_time')
    try:
        schedule_time = datetime.strptime(schedule_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return Response({"error": "Invalid date format. Use '%Y-%m-%d %H:%M:%S'."})
    delay = (schedule_time - datetime.now()).total_seconds()
    threading.Timer(delay, post_to_all, [title, content]).start()
    return Response({"status": "Post scheduled"})
