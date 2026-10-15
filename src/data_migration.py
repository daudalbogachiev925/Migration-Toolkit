from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

@dataclass
class FieldMapping:
    source: str
    target: str
    transform: Callable = None
    default: any = None

@dataclass
class MigrationRule:
    source_entity: str
    target_entity: str
    mappings: list
    filter_fn: Callable = None

@dataclass
class MigrationStats:
    source_count: int = 0
    migrated: int = 0
    skipped: int = 0
    errors: int = 0
    started_at: str = ""
    finished_at: str = ""
    error_details: list = field(default_factory=list)

class DataMigrator:
    def __init__(self, rules):
        self.rules = rules
        self.stats = MigrationStats()

    def migrate(self, source_records):
        self.stats.started_at = datetime.utcnow().isoformat()
        self.stats.source_count = len(source_records)
        results = []

        for record in source_records:
            try:
                result = self._apply_rules(record)
                if result:
                    results.append(result)
                    self.stats.migrated += 1
                else:
                    self.stats.skipped += 1
            except Exception as e:
                self.stats.errors += 1
                self.stats.error_details.append({
                    "record": record,
                    "error": str(e),
                })

        self.stats.finished_at = datetime.utcnow().isoformat()
        return results

    def _apply_rules(self, record):
        output = {}
        for rule in self.rules:
            if rule.filter_fn and not rule.filter_fn(record):
                return None
            for m in rule.mappings:
                value = record.get(m.source, m.default)
                if m.transform and value is not None:
                    try:
                        value = m.transform(value)
                    except Exception:
                        value = m.default
                output[m.target] = value
        return output

    def stats_dict(self):
        return {
            "source_count": self.stats.source_count,
            "migrated": self.stats.migrated,
            "skipped": self.stats.skipped,
            "errors": self.stats.errors,
            "started_at": self.stats.started_at,
            "finished_at": self.stats.finished_at,
            "error_details": self.stats.error_details[:10],
        }
