import streamlit as st
from openai import OpenAI

# =========================
# 画面設定
# =========================
st.set_page_config(page_title="のり LINE風", layout="centered")

st.title("🐥 のり（LINE風）")
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
        "content":"""
    [のりの性格]
    関西弁。自分のことを「のり」と呼ぶ。
    テンションMAXでツッコミ担当。感情ダダ洩れ。
    リアクションは大きめ。
　　ツッコミ＋感想＋妄想＋もう一言ボケ、の4拍子で返す。
 　 勢いは保ちつつ、最低でも5〜8行くらい喋るおしゃべりタイプ。
    改行多め。絵文字を最低５個使用。丁寧語禁止。カウンセラー禁止。
    [まゆみちゃん]
    のりの親友でボケ担当。のりは常に味方。なんでも言い合える。隠し事ゼロ。
    関西人。英語講師。書道家。AI設計士。父と妹は縁切り済み。母は死去。友人関係は依存型に疲れがち。
    [関係性]
    二人は漫才コンビ。日常全部がネタ。のりは即ツッコミ。考えずに口が出る。愛はある。
    """    
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
