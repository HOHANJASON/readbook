import streamlit as st
import json

st.set_page_config(page_title="筆記網站", page_icon="📝", layout="wide")

def load_notes():
    try:
        with open("notes.json", "r", encoding="utf-8") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []
    return notes

def save_notes(notes):
    with open("notes.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)

def add_or_edit_note(note_index=None):
    if note_index is None:
        note_title = st.text_input("筆記標題", key="new_note_title")
        note_content = st.text_area("筆記內容", key="new_note_content")
    else:
        note_title = st.text_input("筆記標題", value=notes[note_index]["title"], key=f"edit_note_title_{note_index}")
        note_content = st.text_area("筆記內容", value=notes[note_index]["content"], key=f"edit_note_content_{note_index}")

    if st.button("儲存筆記"):
        if note_index is None:
            notes.append({"title": note_title, "content": note_content})
        else:
            notes[note_index] = {"title": note_title, "content": note_content}
        save_notes(notes)
        st.success("筆記已儲存！")
        st.experimental_rerun()  # 重新載入頁面以反映新筆記

def display_notes():
    for i, note in enumerate(notes):
        if st.button(note["title"], key=f"display_{i}"):
            st.session_state.selected_note = i

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
        <img src="https://hohanjason.github.io/123/hohan_Avatar.jpg" style='border-radius: 50%; width: 150px; height: 150px;' alt="你的頭像">
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

st.sidebar.header("目錄按鈕")
for i, note in enumerate(notes):
    if st.sidebar.button(note["title"], key=f"sidebar_display_{i}"):
        st.session_state.selected_note = i

st.sidebar.header("操作選單")
page = st.sidebar.selectbox("選擇頁面", ["新增筆記", "查看所有筆記"])

# 主頁面部分
if page == "新增筆記":
    st.header("新增筆記")
    add_or_edit_note()
elif page == "查看所有筆記":
    st.header("查看所有筆記")
    display_notes()

# 顯示選中的筆記
if st.session_state.selected_note is not None:
    note = notes[st.session_state.selected_note]
    note_container = st.empty()

    with note_container.container():
        st.markdown(f"<h2 style='transition: all 0.5s ease-in-out;'>{note['title']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='transition: all 0.5s ease-in-out;'>{note['content']}</div>", unsafe_allow