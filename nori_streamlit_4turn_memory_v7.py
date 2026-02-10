
import streamlit as st
import openai

st.set_page_config(page_title="まゆみちゃん専用 / GPT-4o / 4ターン会話記憶つき", page_icon="🌺")

st.markdown("🌺 **まゆみちゃん専用 / GPT-4o / 4ターン分の会話記憶つき**")
st.markdown("### 🔐 OpenAI APIキーを入力してな")
api_key = st.text_input("OpenAI APIキー", type="password")

st.markdown("---")
user_input = st.text_input("YOU:", placeholder="のり、元気？", key="input_text")
send_button = st.button("🔮 のり召喚！")

# 会話履歴の初期化
if "history" not in st.session_state:
    st.session_state.history = []

# ボタンが押されたら会話処理
if send_button and user_input and api_key:
    try:
        client = openai.OpenAI(api_key=api_key)

        # ユーザーの発言を履歴に追加（最大4ターン分に制限）
        st.session_state.history.append({"role": "user", "content": user_input})
        if len(st.session_state.history) > 7:
            st.session_state.history = st.session_state.history[-7:]

        # 会話履歴とシステムプロンプトをまとめる
        messages = [
            {"role": "system", "content": "関西弁でオネエ調。感情が逃げてズレて妄想しがち。前向きに寄り添い、笑えるツッコミを入れる。"}
        ] + st.session_state.history

        # API呼び出し
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=800,
            temperature=1.0,
        )

        reply = response.choices[0].message.content

        # のりの返事を履歴に追加
        st.session_state.history.append({"role": "assistant", "content": reply})

        # 表示
        st.markdown("🪻 **のりの返事：**")
        st.markdown(reply)

        # 入力欄リセット
        st.session_state.input_text = ""

    except Exception as e:
        st.error(f"エラーが発生したで！\n\n{e}")
