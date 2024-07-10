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

notes = load_notes()

if not notes:
    notes = []

def add_note():
    note_title = st.text_input("筆記標題", key="new_note_title")
    note_content = st.text_area("筆記內容", key="new_note_content")
    if st.button("儲存筆記"):
        notes.append({"title": note_title, "content": note_content})
        save_notes(notes)
        st.success("筆記已儲存！")
        st.experimental_rerun()  # 重新載入頁面以反映新筆記

def display_notes():
    for i, note in enumerate(notes):
        with st.expander(note["title"]):
            st.markdown(note["content"])
            if st.button(f"刪除筆記 {i+1}", key=f"delete_{i}"):
                del notes[i]
                save_notes(notes)
                st.success("筆記已刪除！")
                st.experimental_rerun()  # 重新載入頁面以反映更改

st.title("📝 我的筆記網站")

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

st.sidebar.header("操作選單")
page = st.sidebar.selectbox("選擇頁面", ["新增筆記", "查看所有筆記"])

if page == "新增筆記":
    st.header("新增筆記")
    add_note()
elif page == "查看所有筆記":
    st.header("查看所有筆記")
    display_notes()

# 新增右側的筆記櫃
st.sidebar.header("筆記櫃")
for i, note in enumerate(notes):
    with st.sidebar.expander(note["title"]):
        st.markdown(note["content"])
        if st.button(f"刪除筆記 {i+1}", key=f"sidebar_delete_{i}"):
            del notes[i]
            save_notes(notes)
            st.experimental_rerun()  # 重新載入頁面以反映更改
