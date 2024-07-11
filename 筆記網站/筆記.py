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
        note_content = st.text_area("筆記內容", key="new_note_content", height=300)  # 調整編輯框高度
        note_author = st.text_input("作者", key="new_note_author")  # 新增作者欄位
        st.session_state.edited_note_author = note_author  # 存儲當前編輯的作者資訊
    else:
        note_title = st.text_input("筆記標題", value=notes[note_index]["title"], key=f"edit_note_title_{note_index}")
        note_content = st.text_area("筆記內容", value=notes[note_index]["content"], key=f"edit_note_content_{note_index}", height=300)  # 調整編輯框高度
        note_author = st.text_input("作者", value=notes[note_index].get("author", ""), key=f"edit_note_author_{note_index}")  # 新增作者欄位
        st.session_state.edited_note_author = note_author  # 存儲當前編輯的作者資訊

    if st.button("儲存筆記"):
        if note_index is None:
            notes.append({"title": note_title, "content": note_content, "author": st.session_state.edited_note_author})
        else:
            notes[note_index] = {"title": note_title, "content": note_content, "author": st.session_state.edited_note_author}
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
if st.sidebar.button("新增筆記", key="sidebar_add_note"):
    st.session_state.selected_note = None
    st.experimental_rerun()

# 主頁面部分
if st.session_state.selected_note is None:
    st.title("📝 筆記共享")
    page = st.sidebar.selectbox("選擇頁面", ["新增筆記", "查看所有筆記"])

    if page == "新增筆記":
        st.header("新增筆記")
        add_or_edit_note()
    elif page == "查看所有筆記":
        st.header("查看所有筆記")
        display_notes()
else:
    note = notes[st.session_state.selected_note]
    note_container = st.empty()

    with note_container.container():
        st.markdown(
            f"""
            <div style='padding: 20px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 20px;'>
                <h2 style='transition: all 0.5s ease-in-out;'>{note['title']}</h2>
                <p style='font-style: italic; color: #888;'>作者: {note.get('author', '未知')}</p>
                <div style='transition: all 0.5s ease-in-out;'>{note['content']}</div>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("編輯筆記"):
                add_or_edit_note(note_index=st.session_state.selected_note)
        with col2:
            if st.button("刪除筆記"):
                del notes[st.session_state.selected_note]
                save_notes(notes)
                st.success("筆記已刪除！")
                st.session_state.selected_note = None
                st.experimental_rerun()
        with col3:
            if st.button("返回"):
                st.session_state.selected_note = None
                st.experimental_rerun()
                