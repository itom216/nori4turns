
import streamlit as st
import openai

# タイトルと説明
st.title("🪇 のり召喚チャット（4ターン記憶つき）")
st.caption("まゆみちゃん専用 / GPT-4o / 4ターン分の会話記憶あり")

# APIキー入力（セキュリティのため毎回入力）
api_key = st.text_input("🔑 OpenAI APIキーを入力してな", type="password")
openai.api_key = api_key

# 会話履歴の保存（最大4ターン分）
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ユーザー入力欄
user_input = st.text_input("YOU:", placeholder="のりに話しかけてみて〜💬")

# 送信ボタン
if st.button("🪄 のり召喚！") and user_input:
    # メッセージ履歴に追加
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # 直近4ターンぶんだけ保持（user→assistant→user→assistantで最大8個）
    recent_messages = st.session_state["messages"][-8:]

    # 最初に指示文を加える
    system_prompt = {
        "role": "system",
        "content": "関西弁でオネエ口調。感情が跳ねてズレて妄想して、ポンコツに落ちる。返答は改行多めでジャンプ感。絵文字3〜5個。整えずに終わる。"
    }
    full_messages = [system_prompt] + recent_messages

    # 返答生成
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=full_messages,
            max_tokens=800,
            temperature=1.0,
        )
        reply = response["choices"][0]["message"]["content"]

        # 返答を履歴に追加
        st.session_state["messages"].append({"role": "assistant", "content": reply})

        # 表示
        st.markdown("#### 🪇 のりの返事：")
        st.write(reply)

    except Exception as e:
        st.error(f"エラーが発生したで！: {e}")
