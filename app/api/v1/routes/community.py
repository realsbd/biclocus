from fastapi import APIRouter, Depends, Security

from app.database.dependencies import sessDep
from app.models.auth.functions import authorize, authorize_and_load, authorize_limited
from app.models.auth.token import TokenDecode
from app.models.community import Community
from app.models.community.schemas import CommunityIn, CommunityOut
from app.models.user import User
from app.models.auth.role import Role


router = APIRouter(prefix="/community", tags=["Community"])


@router.post("", response_model=CommunityOut, status_code=201, dependencies=[Security(authorize, scopes=[Role.ADMIN])])
async def create_community(
    community_in: CommunityIn,
    async_session: sessDep,
    token: TokenDecode = Depends(authorize),
):
    if await Community.find(async_session, name=community_in.name, raise_=False):
        raise conflict(msg="Community already exists")
    return await Community(**community_in.model_dump()).save(async_session)


@router.get("", response_model=list[CommunityOut], status_code=200)
async def get_communities(async_session: sessDep):
    return await Community.all(async_session)


@router.get("/{id}", response_model=CommunityOut, status_code=200)
async def get_community(
    async_session: sessDep, id: str, token: TokenDecode = Depends(authorize)
):
    return await Community.find(async_session, id=id, raise_=True)


# @router.get("/rate-limited/{id}", response_model=PostOut, status_code=200)
# async def get_post_rate_limited(
#     async_session: sessDep, id: str, token: TokenDecode = Depends(authorize_limited)
# ):
#     return await Post.find(async_session, id=id, user_id=token.id, raise_=True)


@router.delete("/{id}", status_code=204, dependencies=[Security(authorize, scopes=[Role.ADMIN])])
async def delete_community(
    async_session: sessDep, id: str, token: TokenDecode = Depends(authorize)
):
    community = await Community.find(async_session, id=id, user_id=token.id, raise_=True)
    await community.delete(async_session)  # type: ignore
