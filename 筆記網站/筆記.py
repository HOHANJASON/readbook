import streamlit as st
import json
import os

# 配置網站標題、圖標和版面配置
st.set_page_config(page_title="筆記網站", page_icon="📝", layout="wide")

# 文件路徑
DATA_FILE = 'notes.json'

# 初始化筆記數據
def init_notes():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

# 新增筆記功能
def add_note():
    st.header("新增筆記")
    note_title = st.text_input("筆記標題", key="new_note_title")
    note_content = st.text_area("筆記內容", key="new_note_content")
    if st.button("儲存筆記"):
        notes = load_notes()
        notes.append({"title": note_title, "content": note_content})
        save_notes(notes)
        st.experimental_rerun()

# 顯示所有筆記功能
def display_notes():
    st.header("查看所有筆記")
    notes = load_notes()
    for i, note in enumerate(notes):
        with st.expander(note["title"]):
            st.markdown(note["content"])
            if st.button(f"刪除筆記 {i+1}", key=f"delete_{i}"):
                del notes[i]
                save_notes(notes)
                st.experimental_rerun()

# 查看單一筆記功能
def view_note():
    st.header("查看單一筆記")
    notes = load_notes()
    if 'current_note_index' in st.session_state:
        current_note_index = st.session_state.current_note_index
        st.header(notes[current_note_index]['title'])
        st.markdown(notes[current_note_index]['content'])
    else:
        st.write("請從側邊欄選擇一個筆記查看。")

# 側邊欄的書櫃部分
def show_bookshelf():
    st.sidebar.header("我的書櫃")
    notes = load_notes()
    for i, note in enumerate(notes):
        if st.sidebar.button(f"查看 {note['title']}", key=f"sidebar_view_{i}"):
            st.session_state.current_note_index = i
            st.experimental_rerun()

# 加載筆記數據
def load_notes():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# 保存筆記數據
def save_notes(notes):
    with open(DATA_FILE, 'w') as f:
        json.dump(notes, f)

# 主要流程，呼叫上述功能函數
init_notes()
add_note()
display_notes()
view_note()
show_bookshelf()
