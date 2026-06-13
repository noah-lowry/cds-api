import bisect
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, status
from starlette.datastructures import State as StarletteState

from cds import api, schema
from cds.extraction import load_structured_data  # () -> Map (id, year) CommonDataSet


class CDSAPIState(StarletteState):
    cds_data: dict[tuple[str, str], schema.CommonDataSet]
    institutions: dict[str, api.InstitutionCard]


class CDSAPI(FastAPI):
    state: CDSAPIState


@asynccontextmanager
async def lifespan(app: FastAPI):
    cds_data: dict[tuple[str, str], schema.CommonDataSet] = load_structured_data()

    institutions = {}
    for inst_id, year in cds_data.keys():
        bisect.insort(institutions.setdefault(inst_id, []), year)

    for inst_id, available_years in institutions.items():
        latest_year = max(available_years)
        inst_dataset = cds_data[(inst_id, latest_year)]
        institutions[inst_id] = api.InstitutionCard(
            id=inst_id,
            identity=api.Identity.from_cds(inst_dataset),
            available_years=available_years,
            latest_year=latest_year,
        )

    app.state.cds_data = cds_data
    app.state.institutions = institutions
    yield


app = CDSAPI(lifespan=lifespan)


@app.get("/v1/institutions")
async def get_institutions() -> list[api.InstitutionCard]:
    return sorted(app.state.institutions.values(), key=lambda inst: inst.id)


@app.get("/v1/institutions/{id}")
async def get_institution_by_id(id: str) -> api.InstitutionProfile:
    if id not in app.state.institutions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found"
        )
    latest_year = max(app.state.institutions[id].available_years)
    inst_cds = app.state.cds_data[(id, latest_year)]
    return api.InstitutionProfile.from_cds(inst_cds, id, latest_year)


@app.get("/v1/institutions/{id}/admissions")
async def get_institution_admissions_by_id(id: str) -> api.InstitutionAdmissions:
    if id not in app.state.institutions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found"
        )
    latest_year = max(app.state.institutions[id].available_years)
    inst_cds = app.state.cds_data[(id, latest_year)]
    return api.InstitutionAdmissions.from_cds(inst_cds, id, latest_year)


def serve():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    serve()
