from fastapi import APIRouter

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("")
async def get_all_questions():
    pass


@router.post("")
async def create_question():
    pass
