import streamlit as st
from openai import OpenAI

# =========================
# 画面設定
# =========================
st.set_page_config(page_title="のり LINE風", layout="centered")

st.title("💬 のり（LINE風）")
st.caption("下に入力欄があるで")

# =========================
# APIキー入力（スマホ対応）
# =========================
api_key = st.text_input("🔑 OpenAI APIキー", type="password")
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

# =========================
# 履歴初期化
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# 会話表示（上）
# =========================
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💬 **あなた**\n\n{msg['content']}")
    else:
        st.markdown(f"💄 **のり**\n\n{msg['content']}")

# =========================
# 入力欄（下・LINE風）
# =========================
st.divider()

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "メッセージを入力",
        placeholder="😀のりに話しかけてみてな"
    )
    submitted = st.form_submit_button("送信")

# =========================
# 送信処理
# =========================
if submitted and user_input.strip():

    # ユーザー発言保存
    st.session_state.history.append(
        {"role": "user", "content": user_input}
    )

    # 4ターン制限（8件）
    st.session_state.history = st.session_state.history[-8:]

    # のり人格
    system_prompt = {
        "role": "system",
        "content": (
            "関西弁でオネエ口調。"
            "感情が跳ねてズレて妄想してポンコツに落ちる。"
            "改行多め。リズム感重視。"
            "絵文字は3〜5個。"
            "整えず途中感で終わる。"
        )
    }

    messages = [system_prompt] + st.session_state.history

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1.0,
            max_tokens=800,
        )

        reply = response.choices[0].message.content

        st.session_state.history.append(
            {"role": "assistant", "content": reply}
        )

        # 再描画して下に入力欄を保つ
        st.rerun()

    except Exception as e:
        st.error(f"エラー出たで: {e}")
