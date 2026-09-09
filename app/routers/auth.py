from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, models, schemas, utils, oauth2
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/me", response_model=schemas.UserOut)
def get_current_user_profile(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return current_user


@router.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Normalize email to avoid duplicates with differing cases/whitespace
    normalized_email = (user.email or "").strip().lower()

    existing_user = db.query(models.User).filter(models.User.email == normalized_email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = utils.hash(user.password)
    new_user = models.User(
        email=normalized_email,
        password=hashed_password,
        full_name=getattr(user, "full_name", None),
        bio=getattr(user, "bio", None),
        location=getattr(user, "location", None),
        website=getattr(user, "website", None),
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db.refresh(new_user)

    access_token = oauth2.create_access_token(data={"user_id": new_user.id})
    return schemas.Token(access_token=access_token, token_type="bearer")


#this endpoint is going to be used to login the user. It is going to take the email and password of the user and check if the user exists in the database. If the user exists, it is going to verify the password that the user is trying to login with. If the password is correct, it is going to return a success message. If the password is incorrect, it is going to return an error message.
@router.post("/login", response_model=schemas.Token)
#the OAuth2PasswordRequestForm is a class that is used to get the username and password from the request body. It is going to be used to get the email and password of the user that is trying to login.
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    email = (user_credentials.username or "").strip().lower()
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    #this is going to verify the password that the user is trying to login with. It is going to compare the password that the user is trying to login with and the hashed password that is stored in the database. If they match, it will return True, otherwise it will return False.
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/login_json", response_model=schemas.Token)
def login_json(payload: schemas.UserLogin, db: Session = Depends(database.get_db)):
    email = (payload.email or "").strip().lower()
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not utils.verify(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    payload: dict | None = None,
    db: Session = Depends(database.get_db),
):
    # Minimal refresh flow: use the existing access token to rebuild a token if the caller sends a valid user id.
    # This keeps the frontend from crashing even though the project is not yet using refresh tokens.
    if not payload or not payload.get("refresh_token"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token required")

    token = payload.get("refresh_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token required")

    try:
        decoded = oauth2.verify_access_token(token, HTTPException(status_code=401, detail="Invalid refresh token"))
    except HTTPException:
        raise

    access_token = oauth2.create_access_token(data={"user_id": decoded.id})
    return schemas.Token(access_token=access_token, token_type="bearer")