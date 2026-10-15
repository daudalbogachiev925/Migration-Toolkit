from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from src.compatibility import check_compatibility
from src.platform import list_installed_platforms
from src.data_migration import DataMigrator, MigrationRule, FieldMapping

app = FastAPI(title="Migration Toolkit")

class CompatCheck(BaseModel):
    current: str
    target: str

class MigrateRequest(BaseModel):
    source_entity: str
    target_entity: str
    mappings: List[Dict[str, str]]
    records: List[Dict[str, Any]]

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/platforms")
def platforms():
    return list_installed_platforms()

@app.post("/compatibility")
def compat(req: CompatCheck):
    return check_compatibility(req.current, req.target)

@app.post("/migrate")
def migrate(req: MigrateRequest):
    rule = MigrationRule(
        source_entity=req.source_entity,
        target_entity=req.target_entity,
        mappings=[FieldMapping(**m) for m in req.mappings],
    )
    migrator = DataMigrator([rule])
    result = migrator.migrate(req.records)
    return {"stats": migrator.stats_dict(), "result": result}
