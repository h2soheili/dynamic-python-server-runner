from typing import Optional, Any
from pydantic import BaseModel


class LiveCodeExecution(BaseModel):
    stdout: Optional[str] = None
    output: Optional[str] = None
    time: Optional[str] = None
    memory: Optional[int] = None
    stderr: Optional[Any] = None
    token: Optional[str] = None
    compile_output: Optional[Any] = None
    message: Optional[Any] = None
    status: Optional[Any] = None
