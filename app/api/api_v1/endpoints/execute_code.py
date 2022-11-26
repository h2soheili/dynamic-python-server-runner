import json
from asyncio import sleep
from typing import Any, List
import aiohttp
from fastapi import APIRouter, Depends, HTTPException

from app.schemas import LiveCodeExecution
from app.template.generate_script import generate_script_for_live_coding
from app.utils.global_log import log_factory

router = APIRouter()
logger = log_factory.get_logger(__name__)


@router.post("/", response_model=LiveCodeExecution)
async def execute_code(user_id: str, source_code: str) -> Any:
    async with aiohttp.ClientSession() as session:
        # language_id71 in python 3.7
        # check judge0 http://localhost:2358/languages/
        '''
        add some code for (sdk) for get data
        '''
        data = {
            "source_code": generate_script_for_live_coding(source_code, user_id),
            "language_id": 71
        }
        async with session.post('http://localhost:2358/submissions/?base64_encoded=false&wait=true',
                                data=data) as response:
            try:
                return await response.json()
            except Exception as error:
                return error
