from fastapi import HTTPException, status

def check_if_deleted(item):
    if item.deleted_at != None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Selected item has already been deleted on {item.deleted_at}")