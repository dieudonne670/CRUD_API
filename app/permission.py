from fastapi import HTTPException, status


def verify_owner(owner_id: int, current_user):
    if owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )