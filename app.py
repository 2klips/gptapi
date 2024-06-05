import streamlit as st
import requests
from pymongo import MongoClient
import pandas as pd

mongo_url = 'mongodb+srv://axz1420:dlgusdn113!@ad.1ha4qo7.mongodb.net/?retryWrites=true&w=majority&appName=ad'
client = MongoClient(mongo_url)
database = client['gptapi_ad']
collection = database['ad']

# 프론트엔드

st.title('광고 문구 서비스앱')

generate_url = 'http://127.0.0.1:8000/create_ad'

product_name = st.text_input('제품 이름', '')
details = st.text_input('주요 내용', '')
options = st.multiselect('광고 문구의 느낌', options=['기본', '재밌게', '차분하게', '과장스럽게', '참신하게', '고급스럽게'], default=['기본'])

if st.button('광고 문구 생성하기'):
    try:
        response = requests.post(
            generate_url,
            json={
                "product_name": product_name,
                "details": details,
                "tone_and_manner": ", ".join(options)
            })
        ad = response.json()['ad']
        st.success(ad)

    except:
        st.error("연결 실패!")


result = collection.find()
for i in result:
    st.write('---------------------------------')
    st.write(f'상품 이름 - {i["상품 이름"]}')
    st.write(f'주요 내용 - {i["주요 내용"]}')
    st.write(f'광고 문구의 스타일 - {i["광고 문구의 스타일"]}')
    st.write(f'광고 문구 - {i["광고 문구"]}')
    st.write('---------------------------------')

