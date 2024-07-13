import streamlit as st
import json
import base64
import requests

# GitHub 设置
GITHUB_REPO = "HOHANJASON/readbook"
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # 从 Streamlit 的 Secrets Management 中获取令牌
NOTES_FILE_PATH = "notes_data/notes.json"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{NOTES_FILE_PATH}"

if not GITHUB_TOKEN:
    st.error("GitHub 令牌未设置。请在 Streamlit 的 Secrets Management 中设置 GITHUB_TOKEN。")
    st.stop()

# 加载笔记数据
def load_notes():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json; charset=utf-8'
    }
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        file_content = base64.b64decode(response.json()['content']).decode('utf-8')
        notes = json.loads(file_content)
    else:
        notes = []
    return notes

# 保存笔记数据
def save_notes(notes):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json; charset=utf-8'
    }
    file_content = json.dumps(notes, ensure_ascii=False, indent=4).encode('utf-8')
    base64_content = base64.b64encode(file_content).decode('utf-8')

    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        sha = response.json().get('sha')
        if not sha:
            st.error("无法获取文件的 SHA 值")
            return False
        data = {
            "message": "Update notes",
            "content": base64_content,
            "sha": sha
        }
        response = requests.put(GITHUB_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            st.success("笔记已成功保存到 GitHub！")
            return True
        else:
            st.error(f"保存笔记失败，状态码：{response.status_code}")
            return False
    else:
        st.error(f"无法检索文件的 SHA 值，状态码：{response.status_code}")
        return False

# 添加或编辑笔记
def add_or_edit_note(note_index=None):
    note_key_prefix = "new" if note_index is None else f"edit_{note_index}"
    note_title = st.text_input("笔记标题", value="" if note_index is None else notes[note_index]["title"], key=f"{note_key_prefix}_note_title")
    note_content = st.text_area("笔记内容", value="" if note_index is None else notes[note_index]["content"], key=f"{note_key_prefix}_note_content", height=300)
    note_author = st.text_input("作者", value="" if note_index is None else notes[note_index].get("author", ""), key=f"{note_key_prefix}_note_author")

    if st.button("保存笔记", key=f"{note_key_prefix}_save_note"):
        if note_index is None:
            notes.append({"title": note_title, "content": note_content, "author": note_author})
        else:
            notes[note_index]["title"] = note_title
            notes[note_index]["content"] = note_content
            notes[note_index]["author"] = note_author
        if save_notes(notes):
            st.success("笔记已保存！")
            st.rerun()  # 重新载入页面以反映新笔记

# 显示笔记列表
def display_notes():
    for i, note in enumerate(notes):
        if st.button(note["title"], key=f"display_{i}"):
            st.session_state.selected_note = i

# 主流程
notes = load_notes()

if not notes:
    notes = []

if 'selected_note' not in st.session_state:
    st.session_state.selected_note = None

# 侧边栏部分
st.sidebar.header("作者信息")
st.sidebar.markdown(
    r"""
    <div style='text-align: center; padding-top: 20px;'>
        <img src="https://hohanjason.github.io/123/hohan_Avatar.jpg" style='border-radius: 50%; width: 150px; height: 150px;' alt="你的头像">
        <div style='margin-top: 10px;'>
            <a href="https://www.instagram.com/hohanjason/" target="_blank">
                <button style='margin: 5px;'>Instagram</button>
            </a>
            <a href="https://github.com/HOHANJASON" target="_blank">
                <button style='margin: 5px;'>GitHub</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True
)

st.sidebar.header("目录按钮")
for i, note in enumerate(notes):
    if st.sidebar.button(note["title"], key=f"sidebar_display_{i}"):
        st.session_state.selected_note = i

st.sidebar.header("操作选单")
if st.sidebar.button("新增笔记", key="sidebar_add_note"):
    st.session_state.selected_note = None

# 主页面部分
if st.session_state.selected_note is None:
    st.title("📝 笔记共享")
    page = st.sidebar.selectbox("选择页面", ["新增笔记
