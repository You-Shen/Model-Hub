from flask import Blueprint, Response, json, request, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
import openai
from dashscope import Generation
import dashscope
import requests
import json
from http import HTTPStatus
from models import Conversations, db
from datetime import datetime
messages_chatgpt = []
messages_chatgpt.append({'role': 'user', 'content': "中国首都是哪里？"})
def chat():
    client = openai.OpenAI(
        base_url="https://api.openai-sb.com/v1",
        api_key="sb-6a683cb3bd63a9b72040aa2dd08feff8b68f08a0e1d959f5"
    )
    response = ""
    for resp in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_chatgpt,
            stream=True
    ):
        print(resp.choices[0].delta)
        if resp.choices[0].delta.content is not None:
            content = resp.choices[0].delta.content
            response += content
            json_data = json.dumps({"message": response})
            yield f"data: {json_data}\n\n"
    print("final: "+response)
    # messages_chatgpt.append({'role': 'system', 'content': response})
    # json_data = json.dumps({"message": 'done'})
    # yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
    # return response
for message in chat():
    print(message)