import pandas as pd
import requests

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from postgresql_python_excel_app import crud, models, schemas
from postgresql_python_excel_app.database import SessionLocal, engine

from pathlib import Path
from json import loads


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/clients/", response_model=list[schemas.Client])
def get_clients(skip: int = 0, db: Session = Depends(get_db)):
    return crud.get_clients(db, skip=skip)


@app.get("/clients/{client_id}", response_model=schemas.Client)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client_by_id(db, client_id=client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Client Not Found With Given ID : {client_id}")
    return client


@app.get("/clients/{tckno}", response_model=schemas.Client)
def get_client_by_tckno(tckno: int, db: Session = Depends(get_db)):
    client = crud.get_client_by_tckno(db, tckno=tckno)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Client Not Found With Given TCKNO : {tckno}")
    return client


@app.get("/clients/{status}/", response_model=list[schemas.Client])
def get_clients_by_status(status: str, skip: int = 0, db: Session = Depends(get_db)):
    return crud.get_clients_by_status(db, status=status, skip=skip)


@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    new_client = crud.get_client_by_tckno(db, tckno=client.tckno)
    if new_client:
        raise HTTPException(status_code=400, detail=f"Client Already Registered With Given TCKNO : {client.tckno}")
    return crud.create_client(db, client=client)


@app.post("/clients-bulk/")
def create_client_bulk(excel: schemas.ExcelCreate):
    path = Path(excel.path.replace("/", "//"))
    df = pd.read_excel(path, sheet_name=excel.sheet_name)
    parsed_data = loads(df.to_json(orient="records"))
    response_list = []
    for parsed_object in parsed_data:
        response = requests.post(excel.url, json=parsed_object)
        response_list.append(response.content)
    return response_list


@app.put("/clients/{client_id}", response_model=schemas.Client)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client_to_delete = crud.get_client_by_id(db, client_id=client_id)
    if client_to_delete is None:
        raise HTTPException(status_code=404, detail=f"Client Not Found With Given ID : {client_id}")
    return crud.delete_client(db, client=client_to_delete)


@app.get("/client-infos/", response_model=list[schemas.ClientInfo])
def get_client_infos(skip: int = 0, db: Session = Depends(get_db)):
    return crud.get_client_infos(db, skip=skip)


@app.get("/client-infos/{client_id}/", response_model=list[schemas.ClientInfo])
def get_client_infos_by_client_id(client_id: int, skip: int = 0, db: Session = Depends(get_db)):
    client = crud.get_client_by_id(db, client_id=client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Client Not Found With Given ID : {client_id}")
    return crud.get_client_infos_by_client_id(db, client_id=client_id, skip=skip)


@app.post("/clients/{client_id}/client-infos/", response_model=schemas.ClientInfo)
def create_client_info(client_id: int, client_info: schemas.ClientInfoCreate, db: Session = Depends(get_db)):
    client = crud.get_client_by_id(db, client_id=client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Client Not Found With Given ID : {client_id}")
    return crud.create_client_info(db, client_info=client_info, client_id=client_id)


@app.put("/client-infos/{client_info_id}", response_model=schemas.ClientInfo)
def delete_client_info(client_info_id: int, db: Session = Depends(get_db)):
    client_info_to_delete = crud.get_client_info_by_id(db, client_info_id=client_info_id)
    if client_info_to_delete is None:
        raise HTTPException(status_code=404, detail=f"Client Info Not Found Found With Given ID: {client_info_id}")
    return crud.delete_client_info(db, client_info=client_info_to_delete)


@app.get("/insurances/", response_model=list[schemas.Insurance])
def get_insurances(skip: int = 0, db: Session = Depends(get_db)):
    return crud.get_insurances(db, skip=skip)


@app.get("/insurances/{insurance_id}", response_model=schemas.Insurance)
def get_insurance_by_id(insurance_id: int, db: Session = Depends(get_db)):
    insurance = crud.get_insurance_by_id(db, insurance_id=insurance_id)
    if insurance is None:
        raise HTTPException(status_code=404, detail=f"Insurance Not Found With Given ID: {insurance_id}")
    return insurance


@app.get("/insurances/{client_id}/", response_model=list[schemas.Insurance])
def get_insurances_by_client_id(client_id: int, db: Session = Depends(get_db), skip: int = 0):
    client = crud.get_client_by_id(db, client_id=client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Client Not Found With Given ID : {client_id}")
    return crud.get_insurances_by_client_id(db, client_id=client_id, skip=skip)


@app.get("/insurances-policy/{policy_no}", response_model=schemas.Insurance)
def get_insurance_by_policy_no(policy_no: int, db: Session = Depends(get_db)):
    insurance = crud.get_insurance_by_policy_no(db, policy_no=policy_no)
    if insurance is None:
        raise HTTPException(status_code=404, detail=f"Insurance Not Found With Given POLICY NO: {policy_no}")
    return insurance


@app.post("/clients/{client_id}/insurances/", response_model=schemas.Insurance)
def create_insurance(client_id: int, insurance: schemas.InsuranceCreate, db: Session = Depends(get_db), skip: int = 0):
    client = crud.get_client_by_id(db, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Client Not Found With Given ID : {client_id}")
    client_insurances = crud.get_insurances_by_client_id(db, client_id=client_id, skip=skip)
    for client_insurance in client_insurances:
        if client_insurance.policy_no == insurance.policy_no:
            raise HTTPException(status_code=400,
                                detail=f"Insurance Already Registered With Given POLICY NO : {insurance.policy_no}")
    return crud.create_insurance(db, insurance, client_id=client_id)


@app.put("/insurances/{insurance_id}/", response_model=schemas.Insurance)
def delete_insurance(insurance_id: int, db: Session = Depends(get_db)):
    insurance_to_delete = crud.get_insurance_by_id(db, insurance_id=insurance_id)
    if insurance_to_delete is None:
        raise HTTPException(status_code=404, detail=f"Insurance Not Found Found With Given ID: {insurance_id}")
    return crud.delete_insurance(db, insurance=insurance_to_delete)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)




