from pydantic import BaseModel


class ClientBase(BaseModel):
    name: str
    surname: str
    tckno: int
    date_of_birth: str
    status: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class ClientInfoBase(BaseModel):
    contact_phone: str
    phone_type: str
    e_mail: str
    address: str
    address_province: str
    address_city: str
    status: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class ClientInfoCreate(ClientInfoBase):
    pass


class ClientInfo(ClientInfoBase):
    id: int
    client_id: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class InsuranceBase(BaseModel):
    policy_no: int
    amount: float
    policy_start_date: str
    policy_end_date: str
    insurance_type: str
    status: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class InsuranceCreate(InsuranceBase):
    pass


class Insurance(InsuranceBase):
    id: int
    client_id: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class ExcelBase(BaseModel):
    path: str
    url: str
    sheet_name: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class ExcelCreate(ExcelBase):
    pass


class Excel(ExcelBase):
    id: int
    client_id: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True



