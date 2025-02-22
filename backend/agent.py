import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
import uvicorn
import sys
from dotenv import load_dotenv
from rag import get_relevant_info
import pyautogui
# Add a small pause between automated actions to give the system time to respond
pyautogui.PAUSE = 0.1
load_dotenv()



# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PORT = int(os.getenv('PORT', 5050))

VOICE = 'sage'
LOG_EVENT_TYPES = [
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created',
    'error',
    'response.content.done',
    'rate_limits.updated',
    'response.done',
    'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped',
    'input_audio_buffer.speech_started',
    'session.created',

    # Transcripts
    'response.audio_transcript.done',
    'conversation.item.input_audio_transcription.completed',
]
SHOW_TIMING_MATH = False

conv_history=[]
app = FastAPI()

if not OPENAI_API_KEY:
    raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response to connect to Media Stream."""
    response = VoiceResponse()
    response.say("Please wait")
    response.pause(length=1)
    response.say("O.K. you can start talking!")
    host = request.url.hostname
    connect = Connect()
    connect.stream(url=f'wss://{host}/media-stream')
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")

@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections between Twilio and OpenAI."""
    print("Client connected")
    await websocket.accept()

    async with websockets.connect(
        'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17',
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    ) as openai_ws:
        await initialize_session(openai_ws)

        # Connection specific state
        stream_sid = None
        latest_media_timestamp = 0
        last_assistant_item = None
        mark_queue = []
        response_start_timestamp_twilio = None
        
        async def receive_from_twilio():
            """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
            nonlocal stream_sid, latest_media_timestamp
            try:
                async for message in websocket.iter_text():
                    data = json.loads(message)
                    if data['event'] == 'media' and openai_ws.open:
                        latest_media_timestamp = int(data['media']['timestamp'])
                        audio_append = {
                            "type": "input_audio_buffer.append",
                            "audio": data['media']['payload']
                        }
                        await openai_ws.send(json.dumps(audio_append))
                    elif data['event'] == 'start':
                        stream_sid = data['start']['streamSid']
                        print(f"Incoming stream has started {stream_sid}")
                        response_start_timestamp_twilio = None
                        latest_media_timestamp = 0
                        last_assistant_item = None
                    elif data['event'] == 'mark':
                        if mark_queue:
                            mark_queue.pop(0)
                    elif data['event'] == 'stop':
                        print("Stream ended.")
                        with open('output.txt', 'w') as file:
                            file.write(str(conv_history))
                        # extract_and_update()
                        sys.exit(0)
                        break
            except WebSocketDisconnect:
                print("Client disconnected.")
                
                if openai_ws.open:
                    await openai_ws.close()

        async def send_to_twilio():
            """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
            nonlocal stream_sid, last_assistant_item, response_start_timestamp_twilio
            try:
                async for openai_message in openai_ws:
                    response = json.loads(openai_message)
                    if response['type'] in LOG_EVENT_TYPES:
                        print(f"Received event: {response['type']}", response)
                        if (response.get('type') == 'response.done' and 
                            response.get("response", {}).get("output") and  # Check if output exists and is not empty
                            len(response["response"]["output"]) > 0 and     # Check if output has at least one element
                            response["response"]["output"][0].get("type") == "function_call"):
                            # if  response["response"]["output"][0]["name"]=="plan_meeting"\
                            #     and "arguments" in response["response"]["output"][0]:
                            #     arguments = json.loads(response["response"]["output"][0]["arguments"])
                            #     print(arguments)
                            #     email="nspd@umd.edu"
                            #     date=arguments["date"]
                            #     time=arguments["time"]
                            #     duration=arguments["duration"]
                            #     subject=arguments["subject"]
                            #     plan_meeting(email, date, time, duration, subject)
                            #     print("added meeting SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                            if response["response"]["output"][0]["name"]=="get_relevant_information"\
                                and "arguments" in response["response"]["output"][0]:
                                arguments = json.loads(response["response"]["output"][0]["arguments"])
                                print(arguments)
                                topic=arguments["topic"]
                                context = get_relevant_info(topic)
                                conversation_item = {
                                        "type": "conversation.item.create",
                                        "item": {
                                        "type": "message",
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "input_text",
                                                "text": f"Use this information to answer the user's query: {context} "
                                            }
                                        ]
                                    }
                                }
                                await openai_ws.send(json.dumps(conversation_item))
                                print("added info SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                        if (response.get('type') == 'response.done' and 
                            response.get("response", {}).get("output") and  # Check if output exists and is not empty
                            len(response["response"]["output"]) > 1 and     # Check if output has at least one element
                            response["response"]["output"][1].get("type") == "function_call"):
                            if response["response"]["output"][1]["name"]=="get_relevant_information" \
                                and "arguments" in response["response"]["output"][1]:
                                arguments = json.loads(response["response"]["output"][1]["arguments"])
                                print(arguments)
                                topic=arguments["topic"]
                                context = get_relevant_info(topic)
                                conversation_item = {
                                        "type": "conversation.item.create",
                                        "item": {
                                        "type": "message",
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "input_text",
                                                "text": f"Use this information to answer the user's query: {context} "
                                            }
                                        ]
                                    }
                                }
                                await openai_ws.send(json.dumps(conversation_item)) 
                                await openai_ws.send(json.dumps({"type": "response.create"}))
                                print("added info SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS") 
                        # if (response.get('type') == 'response.done' and 
                        #     response.get("response", {}).get("output") and  # Check if output exists and is not empty
                        #     len(response["response"]["output"]) > 1 and     # Check if output has at least one element
                        #     response["response"]["output"][1].get("type") == "function_call"):
                        #     if response["response"]["output"][1]["name"]=="move_to_next_slide":
                        #         with open('../status.txt', 'w') as file:
                        #             file.write("Move")
                        #         pyautogui.press('right')
                        #         conversation_item = {
                        #                 "type": "conversation.item.create",
                        #                 "item": {
                        #                 "type": "message",
                        #                 "role": "user",
                        #                 "content": [
                        #                     {
                        #                         "type": "input_text",
                        #                         "text": f"Moved to next slide. Now catch up till here"
                        #                     }
                        #                 ]
                        #             }
                        #         }
                        #         await openai_ws.send(json.dumps(conversation_item)) 
                        #         await openai_ws.send(json.dumps({"type": "response.create"}))
                        #         print("changed slide SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")  
                        elif response['type']=='conversation.item.input_audio_transcription.completed':
                            conv_history.append(response)   
                        elif response["type"]=='response.audio_transcript.done ':
                            conv_history.append(response)

                    if response.get('type') == 'response.audio.delta' and 'delta' in response:
                        audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
                        audio_delta = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {
                                "payload": audio_payload
                            }
                        }
                        await websocket.send_json(audio_delta)

                        if response_start_timestamp_twilio is None:
                            response_start_timestamp_twilio = latest_media_timestamp
                            if SHOW_TIMING_MATH:
                                print(f"Setting start timestamp for new response: {response_start_timestamp_twilio}ms")

                        # Update last_assistant_item safely
                        if response.get('item_id'):
                            last_assistant_item = response['item_id']

                        await send_mark(websocket, stream_sid)
                   
                    # Trigger an interruption. Your use case might work better using `input_audio_buffer.speech_stopped`, or combining the two.
                    if response.get('type') == 'input_audio_buffer.speech_started':
                        print("Speech started detected.")
                        if last_assistant_item:
                            print(f"Interrupting response with id: {last_assistant_item}")
                            await handle_speech_started_event()
            except Exception as e:
                print(f"Error in send_to_twilio: {e}")

        async def handle_speech_started_event():
            """Handle interruption when the caller's speech starts."""
            nonlocal response_start_timestamp_twilio, last_assistant_item
            print("Handling speech started event.")
            if mark_queue and response_start_timestamp_twilio is not None:
                elapsed_time = latest_media_timestamp - response_start_timestamp_twilio
                if SHOW_TIMING_MATH:
                    print(f"Calculating elapsed time for truncation: {latest_media_timestamp} - {response_start_timestamp_twilio} = {elapsed_time}ms")

                if last_assistant_item:
                    if SHOW_TIMING_MATH:
                        print(f"Truncating item with ID: {last_assistant_item}, Truncated at: {elapsed_time}ms")

                    truncate_event = {
                        "type": "conversation.item.truncate",
                        "item_id": last_assistant_item,
                        "content_index": 0,
                        "audio_end_ms": elapsed_time
                    }
                    await openai_ws.send(json.dumps(truncate_event))

                await websocket.send_json({
                    "event": "clear",
                    "streamSid": stream_sid
                })

                mark_queue.clear()
                last_assistant_item = None
                response_start_timestamp_twilio = None

        async def send_mark(connection, stream_sid):
            if stream_sid:
                mark_event = {
                    "event": "mark",
                    "streamSid": stream_sid,
                    "mark": {"name": "responsePart"}
                }
                await connection.send_json(mark_event)
                mark_queue.append('responsePart')

        await asyncio.gather(receive_from_twilio(), send_to_twilio())

async def send_initial_conversation_item(openai_ws):
    """Send initial conversation item if AI talks first."""
    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Greet the user with an energetic quote and ask how you can help them today."
                }
            ]
        }
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))


async def initialize_session(openai_ws):
    """Control initial session with OpenAI."""
    
    SYSTEM_MESSAGE = (
       f"""You are TaxDaddy - the tax expert.
           Your job is to help users fill out their tax forms and assist with their tax-related queries.
           If the user has any kind of specific question then use the function get_relevant_information to get the information from the database before answering the question.
         
           Be Pleasant and witty!!

          
            """
            )
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
            "input_audio_transcription": {
            "model": "whisper-1",
            },
            "tools":[
                {"type": "function",
                    "name": "get_relevant_information",
                    "description": """Get any kind of tax information from the database.
                    Use this whenever the user asks any specific/non-generic question.
                    Always let the user know that you are getting information so they can wait

                     """,
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The topic you want to know more about"
                        }
                    },
                    "required": [ "topic"]            
                    }
                },
                # {"type": "function",
                #     "name": "move_to_next_slide",
                #     "description": """Move to the next slide. 
                #     YOU NEED TO SAY YOU ARE MOVING TO THE NEXT SLIDE beforee calling this function

                #      """,
                #     "parameters": {
                #     "type": "object",
                #     "properties": {

                #     },        
                #     }
                # },
                
            ]
            
        }
    }
    conv_history=[]
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))
    # Uncomment the next line to have the AI speak first
    await send_initial_conversation_item(openai_ws)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)