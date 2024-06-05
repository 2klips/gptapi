import streamlit as st
import openai

openai.api_key = 'sk-proj-TcNQOzElFEsZWMnSavDZT3BlbkFJ5DjubM6i8l4U0CktVQxb'

example = {
    "한국어": ["오늘 날씨 어때?", "딥러닝 기반의 AI기술이 인기를 끌고 있다"],
    "영어": ["How's the weather today?", "AI technology based on deep learning is gaining popularity"],
    "일본어": ["今日の天気はどうですか？", "ディープラーニング技術に基づくAI技術が人気を博している"]
}

def translate_text_chatgpt(text, src_lang, trg_lang):
    def build_fewshot(src_lang, trg_lang):
        src_examples = example[src_lang]
        trg_examples = example[trg_lang]

        fewshot_messages = []

        for src_text, trg_text in zip(src_examples, trg_examples):
            fewshot_messages.append({'role': 'user', 'content': src_text})
            fewshot_messages.append({'role': 'assistant', 'content': trg_text})
        return fewshot_messages

    system_instruction = f'assistant는 번역앱으로서 동작한다. {src_lang}을 {trg_lang}으로 적절하게 번역하고, 번역된 텍스트만 출력한다.'
    fewshot_messages = build_fewshot(src_lang=src_lang, trg_lang=trg_lang)

    messages = [{'role':'system', 'content':system_instruction}, *fewshot_messages, {'role':'user', 'content':text}]
    # print(messages)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )

    # print(response)
    # print(response.choices[0].message.content)
    return response.choices[0].message.content


st.title('초간단 번역 서비스앱')
text = st.text_area('번역할 내용을 입력하세요', '')
src_lang = st.selectbox('번역할 언어를 선택하세요', ['한국어', '영어', '일본어'])
trg_lang = st.selectbox('번역될 언어를 선택하세요', ['영어', '한국어', '일본어'])

if st.button('번역하기'):
    translated_text = translate_text_chatgpt(text, src_lang, trg_lang)
    st.success(translated_text)
