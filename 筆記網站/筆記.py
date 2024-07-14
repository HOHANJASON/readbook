import streamlit as st
import json
from pathlib import Path

# 设置页面配置
st.set_page_config(page_title="筆記網站", page_icon="📝", layout="wide")

# 示例翻译函数（需要替换为实际的翻译服务，例如 Google 翻译 API 或 DeepL API）
def translate(text, target_lang):
    if target_lang == 'en':
        # 模拟翻译为英文
        return "Translated to English: " + text
    elif target_lang == 'zh':
        # 模拟翻译为中文
        return "翻譯成中文：" + text
    return text

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

# 添加或编辑笔记
def add_or_edit_note(note_index=None, lang='zh'):
    note_key_prefix = "new" if note_index is None else f"edit_{note_index}"
    note_title_label = "筆記標題" if lang == 'zh' else "Note Title"
    note_content_label = "筆記內容" if lang == 'zh' else "Note Content"
    note_author_label = "作者" if lang == 'zh' else "Author"
    note_file_label = "上傳檔案" if lang == 'zh' else "Upload File"
    note_video_label = "上傳視頻" if lang == 'zh' else "Upload Video"
    note_image_label = "上傳圖片" if lang == 'zh' else "Upload Image"
    save_note_label = "儲存筆記" if lang == 'zh' else "Save Note"
    
    note_title = st.text_input(note_title_label, value="" if note_index is None else notes[note_index]["title"], key=f"{note_key_prefix}_note_title")
    note_content = st.text_area(note_content_label, value="" if note_index is None else notes[note_index]["content"], key=f"{note_key_prefix}_note_content", height=300)
    note_author = st.text_input(note_author_label, value="" if note_index is None else notes[note_index].get("author", ""), key=f"{note_key_prefix}_note_author")
    
    note_file = st.file_uploader(note_file_label, type=["txt", "pdf", "docx"], key=f"{note_key_prefix}_note_file")
    note_video = st.file_uploader(note_video_label, type=["mp4", "avi"], key=f"{note_key_prefix}_note_video")
    note_image = st.file_uploader(note_image_label, type=["jpg", "jpeg", "png"], key=f"{note_key_prefix}_note_image")

    if st.button(save_note_label, key=f"{note_key_prefix}_save_note"):
        note_data = {"title": note_title, "content": note_content, "author": note_author, "files": [], "videos": [], "images": []}
        
        if note_file:
            file_path = save_file(note_file, "files")
            note_data["files"].append(file_path)
        
        if note_video:
            video_path = save_file(note_video, "videos")
            note_data["videos"].append(video_path)
        
        if note_image:
            image_path = save_file(note_image, "images")
            note_data["images"].append(image_path)
        
        if note_index is None:
            notes.append(note_data)
        else:
            notes[note_index].update(note_data)
        
        save_notes(notes)
        if note_index is None:
            st.success("筆記已新增！" if lang == 'zh' else "Note Added!")
        else:
            st.success("筆記已編輯！" if lang == 'zh' else "Note Edited!")
        st.experimental_rerun()  # 重新载入页面以反映新笔记

def save_file(uploaded_file, folder):
    folder_path = Path(folder)
    folder_path.mkdir(exist_ok=True)
    file_path = folder_path / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path)

# 显示笔记列表
def display_notes(lang='zh'):
    for i, note in enumerate(notes):
        if st.button(note["title"], key=f"display_{i}"):
            st.session_state.selected_note = i

# 主流程
notes = load_notes()

if not notes:
    notes = []

if 'selected_note' not in st.session_state:
    st.session_state.selected_note = None

if 'language' not in st.session_state:
    st.session_state.language = 'zh'

lang = st.session_state.language

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
    new_lang = 'en' if lang == 'zh' else 'zh'
    st.session_state.language = new_lang
    # 翻译所有笔记内容
    for note in notes:
        note['title'] = translate(note['title'], new_lang)
        note['content'] = translate(note['content'], new_lang)
        note['author'] = translate(note['author'], new_lang)
    st.experimental_rerun()

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
        add_or_edit_note(lang=lang)
    elif page == ("查看所有筆記" if lang == 'zh' else "View All Notes"):
        st.header("查看所有筆記" if lang == 'zh' else "View All Notes")
        display_notes(lang=lang)
else:
    note = notes[st.session_state.selected_note]
    note_container = st.expander(note["title"], expanded=True)

    with note_container:
        st.markdown(
            f"""
            <div style='padding: 20px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 20px; max-height: 400px; overflow-y: auto;'>
                <h2 style='transition: all 0.5s ease-in-out;'>{note['title']}</h2>
                <p style='font-style: italic; color: #888;'>{("作者: " if lang == 'zh' else "Author: ") + note.get('author', '未知' if lang == 'zh' else 'Unknown')}</p>
                <div style='transition: all 0.5s ease-in-out;'>{note['content']}</div>
            </div>
            """, unsafe_allow_html=True)

        for file in note.get("files", []):
            st.markdown(f"📄 [下載文件]({file})")
        
        for video in note.get("videos", []):
            st.video(video)
        
        for image in note.get("images", []):
            st.image(image)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("編輯筆記" if lang == 'zh' else "Edit Note", key=f"edit_note_{st.session_state .selected_note}"):
                st.session_state.editing_note = st.session_state.selected_note
        with col2 :
            if st.button("刪除筆記" if lang == 'zh' else "Delete Note", key=f"delete_note_{st.session_state.selected_note}"):
                confirm_delete = st.warning("確定要刪除這個筆記嗎？" if lang == 'zh' else "Are you sure you want to delete this note?")
                if confirm_delete:
                    del notes[st.session_state.selected_note]
                    save_notes(notes)
                    st.success("筆記已刪除！" if lang == 'zh' else "Note Deleted!")
                    st.session_state.selected_note = None
                    st.experimental_rerun()  # 重新加载页面
        with col3:
            if st.button("返回" if lang == 'zh' else "Back", key=f"back_to_list"):
                st.session_state.selected_note = None

# 处理编辑笔记的情况
if 'editing_note' in st.session_state:
    add_or_edit_note(note_index=st.session_state.editing_note, lang=lang)
    if st.session_state.selected_note is None:
        del st.session_state.editing_note