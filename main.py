import openai
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import pandas as pd

openai.api_key = 'sk-proj-TcNQOzElFEsZWMnSavDZT3BlbkFJ5DjubM6i8l4U0CktVQxb'
app = FastAPI()

mongo_url = 'mongodb+srv://axz1420:dlgusdn113!@ad.1ha4qo7.mongodb.net/?retryWrites=true&w=majority&appName=ad'
client = MongoClient(mongo_url)
database = client['gptapi_ad']
collection = database['ad']

class AdGenerator:
    def __init__(self, engine='gpt-3.5-turbo'):
        self.engine = engine

    def using_engine(self, prompt):
        system_instruction = f'assistant는 마케팅 문구 생성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라'
        message = [{'role': 'system', 'content': system_instruction}, {'role': 'user', 'content': prompt}]
        response = openai.chat.completions.create(model=self.engine, messages=message)
        result = response.choices[0].message.content.strip()
        return result

    def generate(self, product_name, details, tone_and_manner):
        prompt = f'제품이름: {product_name}\n주요내용: {details}\n광고 문구의 스타일: {tone_and_manner} 위 내용을 참고하여 마케팅 문구를 만들어라'
        result = self.using_engine(prompt=prompt)
        return result

class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str

@app.post("/create_ad")
async def create_ad(product: Product):
    # print(product)
    ad_generator = AdGenerator()
    ad = ad_generator.generate(product_name=product.product_name, details=product.details, tone_and_manner=product.tone_and_manner)

    ad_df = (product.product_name, product.details, [product.tone_and_manner], ad)
    columns = ['상품 이름', '주요 내용', '광고 문구의 스타일', '광고 문구']
    ad_df = pd.DataFrame([ad_df], columns=columns)
    collection.insert_many(ad_df.to_dict(orient='records'))

    return {'ad': ad}







