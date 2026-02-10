
import streamlit as st
import openai

st.set_page_config(page_title="のり（4ターン記憶つき）", page_icon="🪇")

st.title("まゆみちゃん専用 / GPT-4o / 4ターン分の会話記憶つき")
st.caption("🔑 OpenAI APIキーを入力してな")

api_key = st.text_input("OpenAI APIキー", type="password")
if not api_key:
    st.stop()

openai.api_key = api_key

# メモリ保存（最大4ターン分）
if "history" not in st.session_state:
    st.session_state.history = []

# 入力欄の状態管理（ここがポイント！）
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

st.text_input("YOU:", key="user_input", placeholder="のりに話しかけてみて〜💬")

if st.button("🔮 のり召喚！"):
    user_message = st.session_state.user_input

    # 指示文（のり魂）
    system_instruction = (
        "関西弁でオネエ口調。感情が跳ねてズレて妄想して、ポンコツに落ちる。"
        "返答は改行多めでジャンプ感。絵文字3〜5個。整えずに終わる。"
    )

    # メッセージ構築（履歴 + 今回）
    messages = [{"role": "system", "content": system_instruction}]
    messages += st.session_state.history[-7:]  # system除いて最大4ターン（user+assistant=2で1ターン）

    messages.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=800,
            temperature=1.0,
        )
        reply = response["choices"][0]["message"]["content"]
        st.session_state.history.append({"role": "user", "content": user_message})
        st.session_state.history.append({"role": "assistant", "content": reply})

        st.write("🪇 のりの返事：")
        st.write(reply)

        # 入力欄を空にする
        st.session_state.user_input = ""

    except Exception as e:
        st.error(f"エラーが発生したで！\n\n{e}")
