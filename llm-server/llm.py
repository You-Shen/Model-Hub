import re

from flask import after_this_request,Blueprint, Response, json, request, jsonify
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
import sys
import copy
import _thread
import os
from openai import OpenAI
import base64
llm_bp = Blueprint('llm', __name__)
def ensure_system_prompt(messages):
    system_msg_index = next((i for i, m in enumerate(messages) if m['role'] == 'system'), None)
    if system_msg_index is not None:
        messages[system_msg_index]['content'] = current_user.settings.prompt
    else:
        messages.insert(0, {"role": "system", "content": current_user.settings.prompt})
    return messages
@llm_bp.route('/tongyi')
@cross_origin(supports_credentials=True)
@login_required
def getTongyiAnswer():
    if 'tongyi' not in current_user.settings.model_priority.split(','):
        return Response(
        "data: {\"message\": \"未选用该模型\"}\n\n",
        content_type='text/event-stream'
    )
    messages_tongyi = current_user.get_current_tongyi_messages()
    query = request.args.get('query', default='default query')
    messages_tongyi = ensure_system_prompt(messages_tongyi)
    messages_tongyi.append({'role': 'user', 'content': query})

    # 使用列表来收集生成器的输出
    chat_responses = []

    def chat_generator():
        dashscope.api_key = "YOUR API KEY"
        responses = Generation.call(
            model="qwen-turbo",
            messages=messages_tongyi,
            result_format='message',
            stream=True,
            incremental_output=True,
            temperature=current_user.settings.temperature
        )

        whole_message = ""
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                answer_part = response.output.choices[0]['message']['content']
                whole_message += answer_part
                json_data = json.dumps({"message": answer_part})
                yield f"data: {json_data}\n\n"
                sys.stdout.flush()

        messages_tongyi.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"
        sys.stdout.flush()
        print('通义千问结束')

    # 执行生成器并收集响应
    for item in chat_generator():
        chat_responses.append(item)

    # 在生成器执行完毕后设置当前用户的消息
    current_user.set_current_tongyi_messages(messages_tongyi)
    db.session.commit()  # 提交数据库事务
    # print('tesy' + json.dumps(messages_tongyi))

    # 返回响应
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }
    return Response(chat_responses, content_type='text/event-stream', headers=headers)


@llm_bp.route('/chatgpt')
@cross_origin(supports_credentials=True)
@login_required
def get_answer():
    if 'gpt' not in current_user.settings.model_priority.split(','):
        return Response(
        "data: {\"message\": \"未选用该模型\"}\n\n",
        content_type='text/event-stream'
    )
    messages_chatgpt = current_user.get_current_chatgpt_messages()
    query = request.args.get('query', default='default query')
    messages_chatgpt = ensure_system_prompt(messages_chatgpt)
    messages_chatgpt.append({'role': 'user', 'content': query})
    chat_responses = []

    def chat_generator():
        client = openai.OpenAI(
                    base_url="https://api.openai-sb.com/v1",
                    api_key="YOUR API KEY"
                )
        response = ""
        for resp in client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages_chatgpt,
                        stream=True,
                        temperature=current_user.settings.temperature
                ):
                    if resp.choices[0].delta.content is not None:
                        content = resp.choices[0].delta.content
                        response += content
                        json_data = json.dumps({"message": content})
                        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
                        sys.stdout.flush()
        messages_chatgpt.append({'role': 'assistant', 'content': response})
        print('ChatGPT结束')
    for item in chat_generator():
        chat_responses.append(item)
    current_user.set_current_chatgpt_messages(messages_chatgpt)
    db.session.commit()  # 提交数据库事务
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }
    return Response(chat_responses, content_type='text/event-stream', headers=headers)


@llm_bp.route('/wenxin')
@cross_origin(supports_credentials=True)
@login_required
def wenxin_get_answer():
    if 'wenxin' not in current_user.settings.model_priority.split(','):
        return Response(
        "data: {\"message\": \"未选用该模型\"}\n\n",
        content_type='text/event-stream'
    )
    messages_wenxin = current_user.get_current_wenxin_messages()
    query = request.args.get('query', default='default query')
    messages_wenxin = ensure_system_prompt(messages_wenxin)
    messages_wenxin.append({'role': 'user', 'content': query})
    # 使用列表来收集生成器的输出
    chat_responses = []

    def chat_generator():
        url = "https://qianfan.baidubce.com/v2/chat/completions"

        payload = json.dumps({
            "model": "ernie-3.5-8k",
            "messages": messages_wenxin,
            "stream": True,
            "temperature": current_user.settings.temperature
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'YOUR API KEY'
        }

        with requests.post(url, headers=headers, data=payload, stream=True) as r:
            full_response = ""
            for line in r.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith("data:"):
                        try:
                            data = json.loads(line_str[5:])  # 去掉 "data: "
                            delta = data["choices"][0]["delta"]
                            content = delta.get("content", "")
                            full_response += content
                            if content:
                                yield f"data: {json.dumps({'message': content})}\n\n"
                                sys.stdout.flush()
                            if delta.get("finish_reason") == "stop":
                                print("文心一言回复完成")
                        except json.JSONDecodeError:
                            continue
        messages_wenxin.append({'role': 'assistant', 'content': full_response})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
        sys.stdout.flush()
        print(json_data)
        print('文心一言结束')

    # 执行生成器并收集响应
    for item in chat_generator():
        chat_responses.append(item)
    current_user.set_current_wenxin_messages(messages_wenxin)
    db.session.commit()  # 提交数据库事务
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat_responses, content_type='text/event-stream', headers=headers)


# 用户创建新的聊天记录时应该保存旧的聊天记录
@llm_bp.route('/conversations/new_conversation', methods=['POST'])
@cross_origin(supports_credentials=True)
@login_required
def save_and_clear_conversation():
    messages_tongyi, messages_wenxin, messages_chatgpt = current_user.getAllMessages()
    # 检查列表是否为空
    # if not messages_chatgpt or not messages_tongyi or not messages_wenxin:
    if not messages_tongyi and not messages_wenxin and not messages_chatgpt:
        # 列表为空，可以选择返回一个错误响应或者进行其他处理
        return jsonify({'error': 'Some of the message lists are empty.'}), 400

    user_id = current_user.id  # 请替换成你实际的用户 ID
    conversation_id = current_user.conversation_current_id + 1
    current_user.conversation_current_id = conversation_id

    current_timestamp = datetime.utcnow()

    messages_wenxin_cur = current_user.get_current_wenxin_messages()
    messages_tongyi_cur = current_user.get_current_tongyi_messages()
    messages_chatgpt_cur = current_user.get_current_chatgpt_messages()
    #     new_messages = copy.deepcopy(messages_wenxin)
    if len(messages_wenxin_cur) > 1:
        current_summary = messages_wenxin_cur[1]['content'][:10]
    elif len(messages_tongyi_cur) > 1:
        current_summary = messages_tongyi_cur[1]['content'][:10]
    elif len(messages_chatgpt_cur) > 1:
        current_summary = messages_chatgpt_cur[1]['content'][:10]
    else:
        current_summary = "聊天记录"

    # 列表不为空，创建一个新的 Conversations 对象并保存到数据库中
    conversation = Conversations(
        id=conversation_id,
        user_id=user_id,
        chatgpt_messages=json.dumps(messages_chatgpt),  # 转换为 JSON 字符串
        wenxin_messages=json.dumps(messages_wenxin),  # 注意：这里应该是 messages_wenxin 而不是 messages_tongyi
        tongyi_messages=json.dumps(messages_tongyi),
        timestamp=current_timestamp,
        summary=current_summary
    )
    db.session.add(conversation)
    db.session.commit()
    view_conversations()

    # 清空当前对话内容
    messages_chatgpt = []
    messages_tongyi = []
    messages_wenxin = []
    current_user.setAllMessages(messages_chatgpt, messages_tongyi, messages_wenxin)
    db.session.commit()  # 提交数据库事务
    # 返回成功响应或其他适当的响应
    return jsonify({'success': 'Conversation saved successfully.'}), 200


@llm_bp.route('/conversations/update_conversation', methods=['PUT'])
@cross_origin(supports_credentials=True)
@login_required
def update_conversation():
    id = request.args.get('id')
    messages_tongyi, messages_wenxin, messages_chatgpt = current_user.getAllMessages()

    # 检查列表是否为空
    if not messages_chatgpt or not messages_tongyi or not messages_wenxin:
        # 列表为空，可以选择返回一个错误响应或者进行其他处理
        return jsonify({'error': 'Some of the message lists are empty.'}), 400

    user_id = current_user.id  # 请替换成你实际的用户 ID
    conversation = Conversations.query.filter_by(id=id, user_id=user_id)

    messages_wenxin_cur = current_user.get_current_wenxin_messages()
    messages_tongyi_cur = current_user.get_current_tongyi_messages()
    messages_chatgpt_cur = current_user.get_current_chatgpt_messages()
    #     new_messages = copy.deepcopy(messages_wenxin)

    if len(messages_wenxin_cur) >1:
        current_summary = messages_wenxin_cur[1]['content'][:10]
    elif len(messages_tongyi_cur)>1:
        current_summary = messages_tongyi_cur[1]['content'][:10]
    elif  len(messages_chatgpt_cur)>1:
        current_summary = messages_chatgpt_cur[1]['content'][:10]
    else:
        current_summary = "聊天记录"

    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    # 更新消息字段
    Conversations.query.filter_by(id=id, user_id=user_id).update({
        'chatgpt_messages': json.dumps(messages_chatgpt),
        'wenxin_messages': json.dumps(messages_wenxin),
        'tongyi_messages': json.dumps(messages_tongyi),
        'timestamp': datetime.utcnow(),
        'summary': current_summary
    })
    db.session.commit()

    # 清空当前对话内容
    messages_chatgpt = []
    messages_tongyi = []
    messages_wenxin = []
    current_user.setAllMessages(messages_chatgpt, messages_tongyi, messages_wenxin)
    db.session.commit()  # 提交数据库事务
    return jsonify({"message": "Conversation updated successfully"}), 200


# 用户点击某个聊天记录的主题，获取此次聊天记录的所有内容，类似chatgpt页面的功能
# 从页面返回：对话id
# 返回：chatgpt_messages、chatgpt_messages、tongyi_messages
@llm_bp.route('/conversations/get_conversation', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def get_conversation_by_id():
    conversation_id = request.args.get('id')
    user_id = current_user.id

    if not conversation_id or not user_id:
        return jsonify({'error': 'Missing id or user_id'}), 400

    conversation = Conversations.query.filter_by(id=conversation_id, user_id=user_id).first()

    if conversation is None:
        return jsonify({'error': 'Conversation not found'}), 404

    print("messages_chatgpt:", json.loads(conversation.chatgpt_messages))
    print("messages_tongyi:", json.loads(conversation.tongyi_messages))
    print("messages_wenxin:", json.loads(conversation.wenxin_messages))
    messages_chatgpt = json.loads(conversation.chatgpt_messages)
    messages_tongyi = json.loads(conversation.tongyi_messages)
    messages_wenxin = json.loads(conversation.wenxin_messages)
    current_user.setAllMessages(messages_chatgpt, messages_tongyi, messages_wenxin)
    db.session.commit()  # 提交数据库事务

    return jsonify({
        'chatgpt_messages': json.loads(conversation.chatgpt_messages),
        'wenxin_messages': json.loads(conversation.wenxin_messages),
        'tongyi_messages': json.loads(conversation.tongyi_messages)
    }), 200


# 获取当前用户的所有聊天记录的主题
# input：当前用户id 【不需要从页面获取，后端有记录】
# output： conversation.id, conversation.summary

@llm_bp.route('/conversations/get_conversation_summary', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def get_user_conversations():
    user_id = current_user.id
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    # 查询并按 id 从大到小排序,这样查出来的第一个是最近一次的对话主题
    conversations = Conversations.query.filter_by(user_id=user_id).order_by(Conversations.id.desc()).all()

    if not conversations:
        return jsonify({'error': 'No conversations found for this user'}), 404

    result = [
        {'id': conversation.id, 'summary': conversation.summary}
        for conversation in conversations
    ]
    # print(result)
    return jsonify(result), 200


# for test
def view_conversations():
    conversations = Conversations.query.all()
    result = []
    for conversation in conversations:
        result.append({
            'id': conversation.id,
            'user_id': conversation.user_id,
            'chatgpt_messages': conversation.chatgpt_messages,
            'wenxin_messages': conversation.wenxin_messages,
            'tongyi_messages': conversation.tongyi_messages,
            'summary': conversation.summary,
            'timestamp': conversation.timestamp
        })

        print('id:', conversation.id,
              'user_id:', conversation.user_id,
              'chatgpt_messages:', conversation.chatgpt_messages,
              'wenxin_messages:', conversation.wenxin_messages,
              'tongyi_messages:', conversation.tongyi_messages,
              'summary:', conversation.summary,
              'timestamp:', conversation.timestamp)

    return {'conversations': result}


@llm_bp.route('/conversations/delete_conversation', methods=['DELETE'])
@cross_origin(supports_credentials=True)
@login_required
def delete_conversation():
    id = request.args.get('id')
    user_id = current_user.id
    conversation = Conversations.query.filter_by(id=id, user_id=user_id).first()
    if conversation:
        db.session.delete(conversation)
        db.session.commit()
        return jsonify({'message': 'Conversation deleted successfully'}), 200
    else:
        return jsonify({'message': 'Conversation not found'}), 404


@llm_bp.route('/user/settings', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def get_user_settings():
    settings = current_user.settings
    return jsonify({
        'prompt': settings.prompt,
        'temperature': settings.temperature,
        'model_priority': settings.model_priority.split(',')  # 转换为数组返回
    }), 200

@llm_bp.route('/user/settings', methods=['POST'])
@cross_origin(supports_credentials=True)
@login_required
def update_user_settings():
    data = request.json
    settings = current_user.settings

    if not settings:
        return jsonify({'error': 'User settings not found'}), 404

    settings.prompt = data.get('prompt', settings.prompt)
    settings.temperature = data.get('temperature', settings.temperature)
    settings.model_priority = ','.join(data.get('model_priority', ['gpt', 'wenxin', 'tongyi']))

    db.session.commit()

    return jsonify({'message': 'Settings updated successfully'}), 200

@llm_bp.route('/vision', methods=['POST'])
@cross_origin(supports_credentials=True)
@login_required
def vision_analysis():
    data = request.get_json()
    base64_image = data.get('image')
    base64_image = base64_image.split(',')[1]
    if not base64_image:
        return jsonify({'error': '缺少图片数据'}), 400
    try:
        result = analyze_image(base64_image)

        result = re.sub(r'^\s*[\*\-\+] ', '', result, flags=re.MULTILINE)  # 去掉无序列表符号
        result = re.sub(r'^\s*\d+\.\s', '', result, flags=re.MULTILINE)  # 去掉有序列表编号
        result = re.sub(r'(\*|\_){2}(.+?)(\*|\_){2}', r'\2', result)  # 去掉加粗（**text**）
        result = re.sub(r'(\*|\_)(.+?)(\*|\_)', r'\2', result)  # 去掉斜体（*text*）
        print("返回结果： ",result)
        return jsonify({'text': result})
    except Exception as e:
        return jsonify({'error': f'图像分析失败: {str(e)}'}), 500


def analyze_image(base64_image: str) -> str:
    client = OpenAI(
        api_key="YOUR API KEY",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    completion = client.chat.completions.create(
        model="qwen-vl-ocr-latest",
        messages=[
            {
                "role": "system",
                "content": [{"type": "text", "text": """你是一个解析图片中内容的助手，请简要分析传入的图片:
                                                        传入的图片有2种类型：
                                                        - 如果图片是文本或代码内容或以文本或代码内容居多，你就变为图片文字提取器，只返回图片原始内容，不要添加自己的描述。
                                                        - 否则，就简要描述图片中的内容，不要超过100字
                                                        """}]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        "min_pixels": 28 * 28 * 4,
                        "max_pixels": 28 * 28 * 8192
                    },
                    {"type": "text", "text": """你是一个解析图片中内容的助手，请简要分析传入的图片:
                                                        传入的图片有2种类型：
                                                        - 如果图片是文本或代码内容或以文本或代码内容居多，你就变为图片文字提取器，只返回图片原始内容，不要添加自己的描述。
                                                        - 否则，就简要描述图片中的内容，不要超过100字
                                                        """
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return completion.choices[0].message.content
