from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from app.utils.global_log import log_factory

router = APIRouter()
logger = log_factory.get_logger(__name__)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h6>Client Id: 10 (is hard coded in ws://localhost:9000/ws/10)</h1>
        # <form action="" onsubmit="sendMessage(event)">
        #     <input type="text" id="messageText" autocomplete="off"/>
        #     <button>Send</button>
        # </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:9000/ws/10");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(JSON.stringify(event.data))
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/", response_model=Any)
def get() -> Any:
    return HTMLResponse(html)
