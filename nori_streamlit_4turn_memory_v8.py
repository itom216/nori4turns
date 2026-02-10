
import streamlit as st
from openai import OpenAI

# =========================
# 画面設定
# =========================
st.set_page_config(page_title="のり 4ターン記憶つき", layout="centered")

st.title("🐸 のり with 4ターン記憶")
st.caption("まゆみちゃん専用：会話履歴つきStreamlitのり")

# =========================
# APIキー入力
# =========================
api_key = st.sidebar.text_input("OpenAI APIキー", type="password")
if not api_key:
    st.warning("APIキー入れてな〜")
    st.stop()

client = OpenAI(api_key=api_key)

# =========================
# 会話履歴初期化
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# 入力欄
# =========================
user_input = st.text_input("のりに話しかけてみてな❤️", key="input_text")

# =========================
# 送信ボタン
# =========================
if st.button("▶️ のりに話しかける"):
    if user_input.strip() != "":

        # --- ユーザー発言を履歴に追加 ---
        st.session_state.history.append(
            {"role": "user", "content": user_input}
        )

        # --- 最大4ターン（user+assistant=8件）に制限 ---
        if len(st.session_state.history) > 8:
            st.session_state.history = st.session_state.history[-8:]

        # =========================
        # のり人格（system）
        # =========================
        system_prompt = {
            "role": "system",
            "content": (
                "関西弁でオネエ口調。"
                "感情が跳ねてズレて妄想して、"
                "最後はポンコツに落ちる。"
                "返答は改行多めでジャンプ感。"
                "絵文字は3〜5個。"
                "整えずに終わる。"
            )
        }

        # --- system + 直近履歴 ---
        full_messages = [system_prompt] + st.session_state.history

        # =========================
        # API呼び出し
        # =========================
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=full_messages,
                temperature=1.0,
                max_tokens=800,
            )

            assistant_reply = response.choices[0].message.content

            # --- のりの返事を履歴に追加 ---
            st.session_state.history.append(
                {"role": "assistant", "content": assistant_reply}
            )

            st.success("のりの返事：")
            st.markdown(assistant_reply)

        st.rerun()
        
        except Exception as e:
            st.error(f"エラー出たで: {e}")
