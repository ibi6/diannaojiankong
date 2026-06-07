from fastapi import APIRouter

from app.core.responses import success_response

router = APIRouter(tags=["system"])


@router.get("/health")
def health_check():
    return success_response({"status": "ok"})
