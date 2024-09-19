from typing import Dict
from fastapi import APIRouter, HTTPException, Path
from app.services.user_service import get_user_data, ExternalAPIConnectionError


router = APIRouter()


@router.get('/users/{user_id}', response_model=Dict[str, str])
async def get_user(user_id: int = Path(..., gt=0)) -> Dict[str, str]:
    try:
        user_data = await get_user_data(user_id)
        return user_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalAPIConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail='Internal server error')
