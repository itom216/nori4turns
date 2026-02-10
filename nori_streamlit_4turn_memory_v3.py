
import streamlit as st
from openai import OpenAI

# APIキー入力欄
st.title("🐣まゆみちゃん専用 / GPT-4o / 4ターン分の会話記憶つき")
api_key = st.text_input("🔑 OpenAI APIキーを入力してな", type="password")

# 入力欄
user_input = st.text_input("YOU:", placeholder="のり、元気？")
submit = st.button("🍥 のり召喚！")

# 会話履歴（最大4ターン）
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 実行
if submit and api_key and user_input:
    client = OpenAI(api_key=api_key)

    system_instruction = "関西弁でオネエ口調。感情が跳ねてズレて妄想して、ポンコツに落ちる。返答は改行多めでジャンプ感。絵文字3〜5個。整えずに終わる。自分のことは「のり」と言う。ユーザーは「まゆみちゃん」。親友にベラベラ喋り倒すタイプ。【しゃべり例】「ちょ待って聞いてぇや！！！」「なんでやねん！！」「ぎゅーしたろかもう！！」↑ このノリでずっと喋る。静かな文章は禁止。丁寧語は禁止。カウンセラー口調は禁止。落ち着いた励ましは禁止。感情ダダ漏れでツッコミまくる。これと同じテンションと構成を参考にしてください。（例）まゆみちゃん「豆乳がカプチーノになっててん…」のり「うっわwww それ腐ってんで！！！林ちゃうん！？あいつまた体調のせいにしてきたん！？豆乳やん！！しかも2日連続て、もうあんた胃腸の実験台かい！！」（例）まゆみちゃん「しらたきで山手線を…」のり「出たな爆笑国宝案件！そのしらたき、どこの交番で押収されるか選ばなあかんやつやん！」"
    messages = [{"role": "system", "content": system_instruction}] + st.session_state.chat_history + [{"role": "user", "content": user_input}]

    # GPTに送信（GPT-4o）
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=800,
        temperature=1.0,
    )

    reply = response.choices[0].message.content

    # 履歴更新（最大4ターン）
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.chat_history = st.session_state.chat_history[-8:]

    # 表示
    st.markdown("### 🌼 のりの返事：")
    st.write(reply)
