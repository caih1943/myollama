import streamlit as st
import ollama

from gtts.lang import tts_langs
from gtts import gTTS
import base64
from tempfile import NamedTemporaryFile

langs = tts_langs().keys()   #载入所有语言的清单

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
        <audio controls autoplay = "true">
        <source src="data:audio/m3:base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True,
        )


def main():
    st.title("老蔡的对话机器人")
    lang = st.selectbox("请选择发音的语言", options=langs,index=56) # 预设选择简体中文（zh-tw)
    
    #設置用戶輸入框
    user_input = st.text_area("您想问什麼？请输入问题！","")
    
    #當使用者按下送出按鈕後的處理
    if st.button("送出"):
        if user_input:
            #使用ollama模型，進行對話
            response = ollama.chat(model='mistral',messages=[{'role': 'user', 'content': user_input}])
            
            #顯示回答
            st.text("回答：")
            st.write(response['message']['content'])

            tts = gTTS(response['message']['content'], lang=lang,slow=False,lang_check=True)
            with NamedTemporaryFile(suffix=".mp3",delete=False) as temp:
                tempname = temp.name
                tts.save(tempname)
                autoplay_audio(tempname)

        else:
            st.warning("请输入问题！")
            
if __name__ == "__main__":
    main()
