import streamlit as st
import ollama

with open('styles.css', 'r') as f:
    custom_css = f.read()
    st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

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
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

#st.write("# Auto-playing Audio!")
            #Your browser does not support the audio element.
def main():
    #st.title("老蔡的多语种对话机器人")
    st.markdown('<h1 class="custom-title">老蔡的多语种对话机器人(Cai’s multilingual conversational robot)</h1>', unsafe_allow_html=True)
    lang = st.selectbox("请选择发音的语言(Please select the language of pronunciation): ", options=langs, index=56) # 预设选择简体中文    
    model_name = st.selectbox("请选择对话模型(Please select a conversation model): ", ['mistral','qwen','gemma'])
    if model_name == 'mistral':
        model_name = 'mistral'
    elif model_name == 'qwen':
        model_name = 'qwen'
    elif model_name == 'gemma':
        model_name = 'gemma'
    #設置用戶輸入框
    user_input = st.text_area("您想问什麼？请输入问题！(Input question)", "")
    
    #當使用者按下送出按鈕後的處理
    #if st.markdown('<button class="custom-button">送出</button>', unsafe_allow_html=True):
    if st.button('送出(send)'): 
        if user_input:
    #使用ollama模型，進行對話
            response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': user_input}])
            
    #顯示回答
        #st.markdown(f'<p class="custom-text">回答：</p>', unsafe_allow_html=True)
        st.text("回答(Answer)：")
        st.write(response['message']['content'])

        tts = gTTS(response['message']['content'], lang=lang, slow=False, lang_check=True)
        with NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
            temp_file_path = temp.name
            tts.write_to_fp(temp)
            autoplay_audio(temp_file_path)
    else:
        if not user_input:
            st.warning("请输入问题！")
           
if __name__ == "__main__":
    main()