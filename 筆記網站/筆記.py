import streamlit as st
import json
import os
import requests
from requests.auth import HTTPBasicAuth

# GitHub 設置
GITHUB_REPO = "你的用戶名/notes_website"
GITHUB_TOKEN = "你的個人訪問令牌"
NOTES_FILE_PATH = "notes_data/notes.json"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{NOTES_FILE_PATH}"

# 加載筆記數據
def load_notes():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        file_content = json.loads(response.json()['content'])
        notes = json.loads(file_content)
    else:
        notes = []
    return notes

# 保存筆記數據
def save_notes(notes):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    file_content = json.dumps(notes, ensure_ascii=False, indent=4)
    response = requests.get(GITHUB_API_URL, headers=headers)
    sha = response.json()['sha']
    data = {
        "message": "Update notes",
        "content": json.dumps(notes).encode("utf-8").decode("utf-8"),
        "sha": sha
    }
    response = requests.put(GITHUB_API_URL, headers=headers, json=data)
    return response.status_code == 200

# 其餘代碼保持不變...
