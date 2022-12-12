from fastapi import APIRouter

router = APIRouter()


@router.get('/users/', tags=["users"])
async def get_list():
    return [{"transaction": "gekrgeg"}, {"transaction": "123123aagragr"}]


@router.get('/users/{id}', tags=["users"])
async def get(id):
    return {"transaction": f"egregreg with id: {id}"}

