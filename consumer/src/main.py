import streamlit as st
import asyncio
import websockets
import json
import multiprocessing
import socket

# Create an asynchronous function to handle websocket connections
async def handle_websocket(websocket, path):
    print("Handling websocket connection")
    async for message in websocket:
        data = json.loads(message)
        message = data['message']
        st.session_state.messages.append(message)  # Update UI with new message
        await websocket.send(json.dumps({"message": message}))

# Create a function to start the websocket server (for multiprocessing)
def start_server_process():
    print("Starting server process")
    asyncio.run(start_server())

async def start_server():
    async with websockets.serve(handle_websocket, "localhost", 8766):
        print(f"Server started on ws://localhost:8766")
        await asyncio.Future()  # Run forever

# Streamlit UI
st.title("Simple Chat App")

# Initialize session state variables
if 'server_started' not in st.session_state:
    st.session_state.server_started = False
    st.session_state.messages = []
    st.rerun()

user_input = st.text_input("Enter your message:")
send_button = st.button("Send")

# Handle sending messages
if send_button:
    async def send_message():
        async with websockets.connect("ws://localhost:8766") as websocket:
            await websocket.send(json.dumps({"message": user_input}))
    asyncio.run(send_message())

# Display messages
st.markdown("**Chat Messages:**")
st.markdown("\n".join(st.session_state.messages))

# Start the server in a separate process
if not st.session_state.server_started:
    st.session_state.server_started = True
    st.session_state.server_process = multiprocessing.Process(target=start_server_process)
    st.session_state.server_process.start()
