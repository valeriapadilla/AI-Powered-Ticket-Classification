from fastapi import APIRouter, Body
from ..services.github_auth import get_installation_token, get_installation_id
from ..services.github_api import call_github

router = APIRouter(prefix="/gh", tags=["github"])

async def token_for_repo(owner: str, repo: str) -> str:
    installation_id = await get_installation_id(owner)
    return await get_installation_token(installation_id)

@router.get("/{owner}/{repo}/issues/{num}")
async def get_issue(owner: str, repo: str, num: int):
    token = await token_for_repo(owner, repo)
    return await call_github("GET", f"/repos/{owner}/{repo}/issues/{num}", token)

@router.get("/{owner}/{repo}/issues/{num}/comments")
async def list_comments(owner: str, repo: str, num: int):
    token = await token_for_repo(owner, repo)
    return await call_github("GET", f"/repos/{owner}/{repo}/issues/{num}/comments", token)

@router.post("/{owner}/{repo}/issues/{num}/comments")
async def post_comment(owner: str, repo: str, num: int, body: str = Body(..., embed=True)):
    token = await token_for_repo(owner, repo)
    return await call_github(
        "POST", f"/repos/{owner}/{repo}/issues/{num}/comments", token, json={"body": body}
    )

@router.post("/{owner}/{repo}/issues/{num}/labels")
async def add_labels(owner: str, repo: str, num: int, labels: list[str] = Body(..., embed=True)):
    token = await token_for_repo(owner, repo)
    return await call_github(
        "POST", f"/repos/{owner}/{repo}/issues/{num}/labels", token, json={"labels": labels}
    )