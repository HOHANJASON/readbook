import streamlit as st

# 設置頁面配置
st.set_page_config(page_title="筆記網站", page_icon="📝", layout="wide")

# 設置頁面標題
st.title("📝 我的筆記網站")

# 初始化筆記列表
if 'notes' not in st.session_state:
    st.session_state['notes'] = []

# 函數：新增筆記
def add_note():
    note_title = st.text_input("筆記標題", key="new_note_title")
    note_content = st.text_area("筆記內容", key="new_note_content")
    if st.button("儲存筆記"):
        st.session_state.notes.append({"title": note_title, "content": note_content})
        st.experimental_rerun()

# 函數：顯示所有筆記
def display_notes():
    for i, note in enumerate(st.session_state.notes):
        with st.expander(note["title"]):
            st.markdown(note["content"])
            if st.button(f"刪除筆記 {i+1}", key=f"delete_{i}"):
                del st.session_state.notes[i]
                st.experimental_rerun()

# 函數：查看單一筆記
def view_note():
    if 'current_note' in st.session_state:
        st.header(st.session_state.current_note['title'])
        st.markdown(st.session_state.current_note['content'])
    else:
        st.write("請從側邊欄選擇一個筆記查看。")

# 主介面
st.sidebar.header("個人信息")

# 添加圓形框框和按鈕
st.sidebar.markdown(
    """
    <div style='text-align: center; padding-top: 20px;'>
        <img src=r"C:\Users\ㄗ\Desktop\筆記網站\images\hohan_Avatar.jpg" style='border-radius: 50%; width: 150px; height: 150px;' alt="你的頭像">
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

# 操作選單和書櫃
st.sidebar.markdown("<br>", unsafe_allow_html=True)  # 添加空白行

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

st.sidebar.markdown("<br>", unsafe_allow_html=True)  # 添加空白行

st.sidebar.header("我的書櫃")
for i, note in enumerate(st.session_state.notes):
    if st.sidebar.button(f"查看 {note['title']}", key=f"sidebar_view_{i}"):
        st.session_state.current_note = note
        st.experimental_rerun()

# 查看選定的筆記
if 'current_note' in st.session_state:
    st.header(st.session_state.current_note['title'])
    st.markdown(st.session_state.current_note['content'])
