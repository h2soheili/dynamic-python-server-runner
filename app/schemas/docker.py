from typing import Optional
from pydantic import BaseModel


# Shared properties
class DockerImageBase(BaseModel):
    script_name: Optional[str] = None
    script_content: Optional[str] = None
    # state: Optional[str] = None


# Properties to receive on item creation
class DockerImageCreate(DockerImageBase):
    # key: str
    # name: str
    # state: int
    pass


# Properties to receive on item update
class DockerImageUpdate(DockerImageBase):
    pass


# Properties shared by models stored in DB
class DockerImageInDBBase(DockerImageBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class DockerImage(DockerImageInDBBase):
    pass


# Properties properties stored in DB
class DockerImageInDB(DockerImageInDBBase):
    pass
