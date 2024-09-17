from pydantic import BaseModel


class CommunityIn(BaseModel):
    name: str
    description: str
    image: str


class CommunityOut(CommunityIn):
    id: str
