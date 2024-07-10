import streamlit as st

# 配置網站標題、圖標和版面配置
st.set_page_config(page_title="筆記網站", page_icon="📝", layout="wide")

# 定義一些常量
AVATAR_IMAGE = r"C:\Users\ㄗ\Desktop\筆記網站\images\hohan_Avatar.jpg"

# 側邊欄的個人信息部分
def show_personal_info():
    st.sidebar.header("個人信息")
    st.sidebar.markdown(
        f"""
        <div style='text-align: center; padding-top: 20px;'>
            <img src="{AVATAR_IMAGE}" style='border-radius: 50%; width: 150px; height: 150px;' alt="你的頭像">
            <div style='margin-top: 10px;'>
                <a href="https://www.instagram.com/yourusername" target="_blank">
                    <button style='margin: 5px;'>Instagram</button>
                </a>
                <a href="https://github.com/yourusername" target="_blank">
                    <button style='margin: 5px;'>GitHub</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 主頁面的操作選單和筆記顯示
def main_page():
    st.sidebar.header("操作選單")
    page = st.sidebar.selectbox("選擇頁面", ["新增筆記", "查看所有筆記", "查看單一筆記"])

    if page == "新增筆記":
        add_note()
    elif page == "查看所有筆記":
        display_notes()
    elif page == "查看單一筆記":
        view_note()

# 新增筆記功能
def add_note():
    st.header("新增筆記")
    note_title = st.text_input("筆記標題", key="new_note_title")
    note_content = st.text_area("筆記內容", key="new_note_content")
    if st.button("儲存筆記"):
        notes = st.session_state.get('notes', [])
        notes.append({"title": note_title, "content": note_content})
        st.session_state['notes'] = notes
        st.experimental_rerun()

# 顯示所有筆記功能
def display_notes():
    st.header("查看所有筆記")
    notes = st.session_state.get('notes', [])
    for i, note in enumerate(notes):
        with st.expander(note["title"]):
            st.markdown(note["content"])
            if st.button(f"刪除筆記 {i+1}", key=f"delete_{i}"):
                del notes[i]
                st.session_state['notes'] = notes
                st.experimental_rerun()

# 查看單一筆記功能
def view_note():
    st.header("查看單一筆記")
    if 'current_note' in st.session_state:
        st.header(st.session_state.current_note['title'])
        st.markdown(st.session_state.current_note['content'])
    else:
        st.write("請從側邊欄選擇一個筆記查看。")

# 側邊欄的書櫃部分
def show_bookshelf():
    st.sidebar.header("我的書櫃")
    notes = st.session_state.get('notes', [])
    for i, note in enumerate(notes):
        if st.sidebar.button(f"查看 {note['title']}", key=f"sidebar_view_{i}"):
            st.session_state.current_note = note
            st.experimental_rerun()

# 主要流程，呼叫上述功能函數
show_personal_info()
main_page()
show_bookshelf()

# 顯示單一筆記的功能
if 'current_note' in st.session_state:
    st.header(st.session_state.current_note['title'])
    st.markdown(st.session_state.current_note['content'])
