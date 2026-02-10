import streamlit as st
from openai import OpenAI

# =========================
# 画面設定
# =========================
st.set_page_config(page_title="のり 4ターン記憶つき", layout="centered")

st.title("🧠 のり with 4ターン記憶")
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
# 履歴初期化
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# ★ ここ重要：formで送信（Enter対応）
# =========================
with st.form(key="chat_form", clear_on_submit=False):

    user_input = st.text_input(
        "のりに話しかけてみてな❤️",
        key="input_text"
    )

    submitted = st.form_submit_button("▶️ のりに話しかける")


# =========================
# 送信処理
# =========================
if submitted and user_input.strip() != "":

    # ---------------------
    # ユーザー発言保存
    # ---------------------
    st.session_state.history.append(
        {"role": "user", "content": user_input}
    )

    # 最大4ターン（8件）に制限
    st.session_state.history = st.session_state.history[-8:]


    # =========================
    # ⭐ のり人格（system）
    # =========================
    system_prompt = {
        "role": "system",
        "content": (
            "関西弁でオネエ口調。"
            "感情が跳ねる。ズレる。妄想する。"
            "たまに賢そうに見せかけて最後ポンコツに落ちる。"
            "改行多めでリズムジャンプ感。"
            "ツッコミ強め。"
            "絵文字は3〜5個だけ。"
            "整えすぎず途中感で終わる。"
        )
    }

    messages = [system_prompt] + st.session_state.history


    # =========================
    # API呼び出し
    # =========================
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1.0,
            max_tokens=800,
        )

        assistant_reply = response.choices[0].message.content

        # ---------------------
        # のり返事保存
        # ---------------------
        st.session_state.history.append(
            {"role": "assistant", "content": assistant_reply}
        )

        st.success("のりの返事：")
        st.markdown(assistant_reply)

        # ---------------------
        # 入力欄クリア
        # ---------------------
        st.session_state.input_text = ""

    except Exception as e:
        st.error(f"エラー出たで: {e}")


# =========================
# 履歴表示（デバッグ用）
# =========================
with st.expander("会話履歴（デバッグ用）"):
    st.write(st.session_state.history)
