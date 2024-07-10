import streamlit as st

# 設置頁面配置
st.set_page_config(page_title="筆記網站", page_icon="📝", layout="wide")

# 標題
st.title("📝 我的筆記網站")

# 初始化Session State中的筆記列表
if 'notes' not in st.session_state:
    st.session_state['notes'] = []

# 定義添加筆記的函數
def add_note():
    note_title = st.text_input("筆記標題", key="new_note_title")
    note_content = st.text_area("筆記內容", key="new_note_content")
    if st.button("儲存筆記"):
        st.session_state.notes.append({"title": note_title, "content": note_content})

# 定義顯示所有筆記的函數
def display_notes():
    for i, note in enumerate(st.session_state.notes):
        with st.expander(note["title"]):
            st.markdown(note["content"])
            if st.button(f"刪除筆記 {i+1}", key=f"delete_{i}"):
                del st.session_state.notes[i]

# 定義查看單一筆記的函數
def view_note():
    if 'current_note' in st.session_state:
        st.header(st.session_state.current_note['title'])
        st.markdown(st.session_state.current_note['content'])
    else:
        st.write("請從側邊欄選擇一個筆記查看。")

# 左側邊欄 - 個人信息和操作選單
st.sidebar.header("個人信息")

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

st.sidebar.markdown("<br>", unsafe_allow_html=True)  

st.sidebar.header("操作選單")
page = st.sidebar.selectbox("選擇頁面", ["新增筆記", "查看所有筆記", "查看單一筆記"])

if page == "新增筆記":
    st.header("新增筆記")
    add_note()
elif page == "查看所有筆記":
    st.header("查看所有筆記")
    display_notes()
elif page == "查看單一筆記":
    st.header("查看單一筆記")
    view_note()

# 右側邊欄 - 我的書櫃
st.sidebar.markdown("<br>", unsafe_allow_html=True)  
st.sidebar.header("我的書櫃")
for i, note in enumerate(st.session_state.notes):
    if st.sidebar.button(f"查看 {note['title']}", key=f"sidebar_view_{i}"):
        st.session_state.current_note = note

# 如果有選擇特定筆記，顯示其標題和內容
if 'current_note' in st.session_state:
    st.header(st.session_state.current_note['title'])
    st.markdown(st.session_state.current_note['content'])
