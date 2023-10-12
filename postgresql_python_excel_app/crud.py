from sqlalchemy.orm import Session

from . import models, schemas


def get_client_by_id(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_tckno(db: Session, tckno: int):
    return db.query(models.Client).filter(models.Client.tckno == tckno).first()


def get_clients_by_status(db: Session, status: str, skip: int = 0):
    return db.query(models.Client).filter(models.Client.status == status).offset(skip).all()


def get_clients(db: Session, skip: int = 0):
    return db.query(models.Client).offset(skip).all()


def create_client(db: Session, client: schemas.ClientCreate):
    new_client = models.Client(**client.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


def delete_client(db: Session, client: schemas.Client):
    client.status = "D"

    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_client_info_by_id(db: Session, client_info_id: int):
    return db.query(models.ClientInfo).filter(models.ClientInfo.id == client_info_id).first()


def get_client_infos_by_client_id(db: Session, client_id: int, skip: int = 0):
    return db.query(models.ClientInfo).filter(models.ClientInfo.client_id == client_id).offset(skip).all()


def get_client_infos(db: Session, skip: int = 0):
    return db.query(models.ClientInfo).offset(skip).all()


def create_client_info(db: Session, client_info: schemas.ClientInfoCreate, client_id: int):
    new_client_info = models.ClientInfo(**client_info.model_dump(), client_id=client_id)
    db.add(new_client_info)
    db.commit()
    db.refresh(new_client_info)
    return new_client_info


def delete_client_info(db: Session, client_info: schemas.ClientInfo):
    client_info.status = "D"
    db.add(client_info)
    db.commit()
    db.refresh(client_info)
    return client_info


def get_insurances(db: Session, skip: int = 0):
    return db.query(models.Insurance).offset(skip).all()


def get_insurance_by_id(db: Session, insurance_id: int):
    return db.query(models.Insurance).filter(models.Insurance.id == insurance_id).first()


def get_insurances_by_client_id(db: Session, client_id: int, skip: int = 0):
    return db.query(models.Insurance).filter(models.Insurance.client_id == client_id).offset(skip).all()


def get_insurance_by_policy_no(db: Session, policy_no: int):
    return db.query(models.Insurance).filter(models.Insurance.policy_no == policy_no).first()


def create_insurance(db: Session, insurance: schemas.InsuranceCreate, client_id: int):
    new_insurance = models.Insurance(**insurance.model_dump(), client_id=client_id)
    db.add(new_insurance)
    db.commit()
    db.refresh(new_insurance)
    return new_insurance


def delete_insurance(db: Session, insurance: schemas.Insurance):
    insurance.status = "D"
    db.add(insurance)
    db.commit()
    db.refresh(insurance)
    return insurance




