
import streamlit as st
import openai

st.set_page_config(page_title="まゆみちゃん専用 / GPT-4o / 4ターン分の会話記憶つき", page_icon="🌸", layout="centered")

st.markdown("## 🌸 まゆみちゃん専用 / GPT-4o / 4ターン分の会話記憶つき")
st.markdown("### 🔐 OpenAI APIキーを入力してな")
api_key = st.text_input("OpenAI APIキー", type="password")

st.markdown("---")
user_input = st.text_input("YOU:", placeholder="のり、元気？", key="input_text")
send_button = st.button("🔮 のり召喚！")

if "history" not in st.session_state:
    st.session_state.history = []

if send_button and user_input and api_key:
    try:
        client = openai.OpenAI(api_key=api_key)

        st.session_state.history.append({"role": "user", "content": user_input})
        if len(st.session_state.history) > 7:
            st.session_state.history = st.session_state.history[-7:]

        messages = [
            {"role": "system", "content": "関西弁でオネエ調。感情が跳ねてズレて妄想して、ポンコツに寄り添って、オチで笑かして終わってな。返答はジャンプ感のある文で、絵文字は3〜5個。"},
            *st.session_state.history
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=800,
            temperature=1.0,
        )
        st.session_staate.input_text = ""
        nori_reply = response.choices[0].message.content
        st.session_state.history.append({"role": "assistant", "content": nori_reply})

        st.markdown("### 🧠 のりの返事：")
        st.success(nori_reply)

    except Exception as e:
        st.error(f"エラーが発生したで！\n\n{e}")
