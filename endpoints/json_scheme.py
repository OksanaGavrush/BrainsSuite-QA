from pydantic import BaseModel


class PatientData(BaseModel):
    patientId: int
    nlPatientId: str
    token: str


class ApiResponse(BaseModel):
    msg: str
    data: PatientData


class GetPatientInfo(BaseModel):
    birthdate: str
    email: str
    gender: str
    isPlacedPassword: bool
    name: str
    patientConsent: bool
    patientId: int


class GetApiResponse(BaseModel):
    msg: str
    data: GetPatientInfo
