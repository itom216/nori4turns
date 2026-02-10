
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os

st.set_page_config(page_title="のり 4ターン記憶つき", layout="centered")

st.title("🐕 のり with 4ターン記憶")
st.caption("まゆみちゃん専用：会話履歴つきStreamlitのり")

api_key = st.sidebar.text_input("OpenAI APIキー", type="password")
if not api_key:
    st.warning("APIキーを入力してな")
    st.stop()

client = OpenAI(api_key = api_key)

# セッション状態に履歴がなければ初期化
if "history" not in st.session_state:
    st.session_state.history = []

# ユーザー入力
user_input = st.text_input("のりに話しかけてみてな❤️", key="input_text")

# 送信ボタン
if st.button("▶️ のりに話しかける"):
    if user_input.strip() != "":
        # 会話履歴に追加（最大4ターンぶん）
        st.session_state.history.append({"role": "user", "content": user_input})
        if len(st.session_state.history) > 8:
            st.session_state.history = st.session_state.history[-8:]

        # API呼び出し
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.history,
                temperature=1.0,
                max_tokens=800,
            )
            assistant_reply = response.choices[0].message.content
            st.session_state.history.append({"role": "assistant", "content": assistant_reply})
            st.success("のりの返事：")
            st.markdown(assistant_reply)
            # 入力欄を空にする
            st.session_state.input_text = ""
        except Exception as e:
            st.error(f"エラーが起きたで: {e}")
