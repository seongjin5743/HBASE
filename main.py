from fastapi import FastAPI
import happybase
from pydantic import BaseModel
import uuid
from datetime import datetime

# 채팅방 생성 요청 데이터를 검증하기 위한 Pydantic 모델
class Chatroom(BaseModel):
    room_name: str  # 채팅방 이름

# 메시지 생성 요청 데이터를 검증하기 위한 Pydantic 모델
class Message(BaseModel):
    room_id: str  # 메시지가 속한 채팅방 ID
    content: str  # 메시지 내용

# HBase 서버와 연결 설정
connection = happybase.Connection('localhost', port=9090)  # HBase 서버 주소 및 포트
connection.open()  # 연결 열기

# FastAPI 애플리케이션 초기화
app = FastAPI()

# 서버 상태 확인
@app.get('/')
def index():
    return {'Hello': 'World'}  # 간단한 응답 반환

# 채팅방 생성
@app.post('/chatrooms')
def create_chatroom(chatroom: Chatroom):
    table = connection.table('chatrooms')  # 'chatrooms' 테이블 접근
    chatroom_id = str(uuid.uuid4())  # 고유한 채팅방 ID 생성
    # HBase에 채팅방 데이터 저장
    table.put(chatroom_id, {'info:room_name': chatroom.room_name})

    return {'chatroom_id': chatroom_id, 'chatroom_name': chatroom.room_name}  # 생성된 채팅방 정보 반환

# 채팅방 목록 조회
@app.get('/chatrooms')
def get_chatrooms():
    table = connection.table('chatrooms')  # 'chatrooms' 테이블 접근
    rows = table.scan()  # 테이블의 모든 데이터 스캔
    result = []
    for k, v in rows:
        # 각 채팅방 데이터를 리스트에 추가
        result.append({'chatroom_id': k, 'chatroom_name': v[b'info:room_name']})
    return result  # 채팅방 목록 반환

# 메시지 생성
@app.post('/messages')
def create_message(message: Message):
    table = connection.table('messages')  # 'messages' 테이블 접근
    room_id = message.room_id  # 요청에서 채팅방 ID 가져오기
    timestamp = int(datetime.now().timestamp() * 1000)  # 현재 시간을 밀리초 단위로 변환
    message_id = f'{room_id}-{timestamp}'  # 고유 메시지 ID 생성
    # HBase에 메시지 데이터 저장
    table.put(message_id, {'info:content': message.content, 'info:room_id': room_id})
    return {'message_id': message_id, 'room_id': room_id, 'content': message.content}  # 생성된 메시지 정보 반환

# 특정 채팅방의 메시지 조회
@app.get('/chatrooms/{room_id}/messages')
def get_messages(room_id: str):
    table = connection.table('messages')  # 'messages' 테이블 접근
    prefix = room_id.encode('utf-8')  # 채팅방 ID를 접두사로 설정
    rows = table.scan(row_prefix=prefix, reverse=True)  # 해당 채팅방의 메시지 역순 조회
    result = []
    for k, v in rows:
        # 각 메시지 데이터를 리스트에 추가
        result.append({'message_id': k, 'room_id': v[b'info:room_id'], 'content': v[b'info:content']})
    return result  # 메시지 목록 반환