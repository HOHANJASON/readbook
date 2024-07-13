import streamlit as st
import json

# 设置页面配置
st.set_page_config(page_title="筆記網站", page_icon="📝", layout="wide")

# 加载笔记数据
def load_notes():
    try:
        with open("notes.json", "r", encoding="utf-8") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []
    return notes

# 保存笔记数据
def save_notes(notes):
    with open("notes.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)

# 加载便利贴数据
def load_sticky_notes():
    try:
        with open("sticky_notes.json", "r", encoding="utf-8") as file:
            sticky_notes = json.load(file)
    except FileNotFoundError:
        sticky_notes = []
    return sticky_notes

# 保存便利贴数据
def save_sticky_notes(sticky_notes):
    with open("sticky_notes.json", "w", encoding="utf-8") as file:
        json.dump(sticky_notes, file, ensure_ascii=False, indent=4)

# 添加或编辑笔记
def add_or_edit_note(note_index=None, lang='zh'):
    note_key_prefix = "new" if note_index is None else f"edit_{note_index}"
    note_title_label = "筆記標題" if lang == 'zh' else "Note Title"
    note_content_label = "筆記內容" if lang == 'zh' else "Note Content"
    note_author_label = "作者" if lang == 'zh' else "Author"
    save_note_label = "儲存筆記" if lang == 'zh' else "Save Note"
    
    notes = load_notes()
    note_title = st.text_input(note_title_label, value="" if note_index is None else notes[note_index]["title"], key=f"{note_key_prefix}_note_title")
    note_content = st.text_area(note_content_label, value="" if note_index is None else notes[note_index]["content"], key=f"{note_key_prefix}_note_content", height=300)
    note_author = st.text_input(note_author_label, value="" if note_index is None else notes[note_index].get("author", ""), key=f"{note_key_prefix}_note_author")

    if st.button(save_note_label, key=f"{note_key_prefix}_save_note"):
        if note_index is None:
            notes.append({"title": note_title, "content": note_content, "author": note_author})
        else:
            notes[note_index]["title"] = note_title
            notes[note_index]["content"] = note_content
            notes[note_index]["author"] = note_author
        save_notes(notes)
        st.success("筆記已儲存！" if lang == 'zh' else "Note Saved!")
        st.experimental_rerun()  # 重新载入页面以反映新笔记

# 添加或编辑便利贴
def add_or_edit_sticky_note():
    sticky_notes = load_sticky_notes()
    sticky_note_title = st.text_input("便利貼標題")
    sticky_note_content = st.text_area("便利貼內容", height=300)

    if st.button("儲存便利貼"):
        sticky_notes.append({"title": sticky_note_title, "content": sticky_note_content})
        save_sticky_notes(sticky_notes)
        st.success("便利貼已儲存！")
        st.experimental_rerun()

# 显示便利贴
def display_sticky_notes():
    sticky_notes = load_sticky_notes()
    for i, sticky_note in enumerate(sticky_notes):
        st.markdown(f"### {sticky_note['title']}")
        st.markdown(sticky_note["content"])
        if st.button("刪除", key=f"delete_sticky_{i}"):
            del sticky_notes[i]
            save_sticky_notes(sticky_notes)
            st.success("便利貼已刪除！")
            st.experimental_rerun()

# 显示所有笔记
def display_notes(lang='zh'):
    notes = load_notes()
    for i, note in enumerate(notes):
        st.markdown(f"### {note['title']}")
        st.markdown(
            f"""
            <p style='font-style: italic; color: #888;'>{("作者: " if lang == 'zh' else "Author: ") + note.get('author', '未知' if lang == 'zh' else 'Unknown')}</p>
            <div style='transition: all 0.5s ease-in-out;'>{note['content']}</div>
            """
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("編輯筆記" if lang == 'zh' else "Edit Note", key=f"edit_note_{i}"):
                st.session_state.selected_note = i
        with col2:
            if st.button("刪除筆記" if lang == 'zh' else "Delete Note", key=f"delete_note_{i}"):
                del notes[i]
                save_notes(notes)
                st.success("筆記已刪除！" if lang == 'zh' else "Note Deleted!")
                st.experimental_rerun()  # 重新加载页面
        with col3:
            if st.button("返回" if lang == 'zh' else "Back", key=f"back_to_list_{i}"):
                st.session_state.selected_note = None

# 主流程
notes = load_notes()
sticky_notes = load_sticky_notes()

if not notes:
    notes = []

if 'selected_note' not in st.session_state:
    st.session_state.selected_note = None

if 'language' not in st.session_state:
    st.session_state.language = 'zh'

if 'page' not in st.session_state:
    st.session_state.page = "notes"

lang = st.session_state.language

# 导航栏部分
st.markdown(
    """
    <style>
        .nav-bar {
            display: flex;
            justify-content: space-around;
            padding: 10px;
            background-color: #f0f0f0;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }
        .nav-bar a {
            text-decoration: none;
            color: #333;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <div class='nav-bar'>
        <a href="#" onclick="window.location.hash='notes'; window.location.reload();">筆記共享</a>
        <a href="#" onclick="window.location.hash='sticky_notes'; window.location.reload();">便利貼</a>
    </div>
    """, unsafe_allow_html=True
)

# 侧边栏部分
st.sidebar.header("作者信息" if lang == 'zh' else "Author Information")
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

# 语言切换按钮
if st.sidebar.button("切換至英文" if lang == 'zh' else "Switch to Chinese"):
    st.session_state.language = 'en' if lang == 'zh' else 'zh'
    st.experimental_rerun()

# 笔记功能部分
if st.session_state.page == "notes":
    st.sidebar.header("目錄按鈕" if lang == 'zh' else "Note List")
    for i, note in enumerate(notes):
        if st.sidebar.button(note["title"], key=f"sidebar_display_{i}"):
            st.session_state.selected_note = i

    st.sidebar.header("操作選單" if lang == 'zh' else "Actions")
    if st.sidebar.button("新增筆記" if lang == 'zh' else "Add Note", key="sidebar_add_note"):
        st.session_state.selected_note = None
        st.session_state.editing_note = None

    # 主页面部分
    if st.session_state.selected_note is None:
        st.title("📝 筆記共享" if lang == 'zh' else "📝 Note Sharing")
        page = st.sidebar.selectbox("選擇頁面" if lang == 'zh' else "Select Page", ["新增筆記" if lang == 'zh' else "Add Note", "查看所有筆記" if lang == 'zh' else "View All Notes"])

        if page == ("新增筆記" if lang == 'zh' else "Add Note"):
            st.header("新增筆記" if lang == 'zh' else "Add Note")
            add_or_edit_note()
        elif page == ("查看所有筆記" if lang == 'zh' else "View All Notes"):
            st.header("所有筆記" if lang == 'zh' else "All Notes")
            display_notes(lang=lang)
    else:
        st.title(notes[st.session_state.selected_note]["title"])
        display_notes(lang=lang)

# 便利贴功能部分
elif st.session_state.page == "sticky_notes":
    st.title("📌 便利貼" if lang == 'zh' else "📌 Sticky Notes")
    page = st.sidebar.selectbox("選擇頁面", ["新增便利貼", "查看所有便利貼"])

    if page == "新增便利貼":
        st.header("新增便利貼")
        add_or_edit_sticky_note()
    elif page == "查看所有便利貼":
        st.header("所有便利貼")
        display_sticky_notes()