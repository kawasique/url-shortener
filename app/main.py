from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import Response, RedirectResponse
from settings import OFFSET, LETTERS, INV_LETTERS
from db import engine, get_db
from auth import verify_key
import models


models.Base.metadata.create_all(engine)


app = FastAPI(swagger_ui_parameters={"persistAuthorization": True})


def id_to_key(id: int) -> str:
    # https://en.wikipedia.org/wiki/Lehmer_random_number_generator
    assert (id > 0) and (id < (0x7FFFFFFF - 1))

    value = (OFFSET + id) * 0xBC8F % 0x7FFFFFFF

    result = []
    while value > 0:
        value, letter = divmod(value, len(LETTERS))
        result.append(LETTERS[letter])
    return "".join(result)


def key_to_id(value: str):
    result = 0
    for k, v in enumerate(value):
        result += pow(len(LETTERS), k) * INV_LETTERS[v]

    return result * 0x713CEE3F % 0x7FFFFFFF - OFFSET


@app.get("/healthcheck", tags=["Misc"])
async def healthcheck():
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/entries",
    response_model=models.EntryOut,
    dependencies=[Depends(verify_key)],
)
def create_entry(entry: models.EntryIn, db: Session = Depends(get_db)):
    instance = models.Entry(url=str(entry.url))

    db.add(instance)
    db.commit()

    return {"url": instance.url, "key": id_to_key(instance.id)}


@app.get(
    "/entries/{entry_key}",
    response_model=models.EntryOut,
    dependencies=[Depends(verify_key)],
)
def get_entry(entry_key: str, db: Session = Depends(get_db)):
    entry_id = key_to_id(entry_key)

    instance = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if instance == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")

    return {"url": instance.url, "key": entry_key}


@app.get(
    "/entries",
    response_model=list[models.EntryOut],
    dependencies=[Depends(verify_key)],
)
def get_entries(db: Session = Depends(get_db)):
    entries = db.query(models.Entry).all()

    return [{"url": e.url, "key": id_to_key(e.id)} for e in entries]


@app.delete(
    "/entries/{entry_key}",
    dependencies=[Depends(verify_key)],
)
def delete_entry(entry_key: str, db: Session = Depends(get_db)):
    entry_id = key_to_id(entry_key)

    instance = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if instance == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.delete(instance)
    db.commit()

    return Response(status_code=status.HTTP_200_OK)


@app.get("/{entry_key}")
def redirect(entry_key: str, db: Session = Depends(get_db)):
    entry_id = key_to_id(entry_key)

    instance = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if instance == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")

    return RedirectResponse(url=instance.url)
