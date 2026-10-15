import json
from datetime import datetime

def migration_report(migrator, path="migration_report.json"):
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "stats": migrator.stats_dict(),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report

def etl_report(pipeline, path="etl_report.json"):
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "stats": pipeline.stats_dict(),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report
