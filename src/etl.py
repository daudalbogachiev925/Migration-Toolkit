from dataclasses import dataclass
from typing import Callable
from datetime import datetime
import csv
import json
from pathlib import Path

@dataclass
class ETLStats:
    extracted: int = 0
    transformed: int = 0
    loaded: int = 0
    failed: int = 0
    started_at: str = ""
    finished_at: str = ""

class ETLPipeline:
    def __init__(self):
        self.extractors = []
        self.transformers = []
        self.loaders = []
        self.stats = ETLStats()

    def add_extractor(self, fn):
        self.extractors.append(fn)
        return self

    def add_transformer(self, fn):
        self.transformers.append(fn)
        return self

    def add_loader(self, fn):
        self.loaders.append(fn)
        return self

    def run(self):
        self.stats.started_at = datetime.utcnow().isoformat()
        data = []
        for ext in self.extractors:
            chunk = ext()
            data.extend(chunk if isinstance(chunk, list) else [chunk])
        self.stats.extracted = len(data)

        for tr in self.transformers:
            data = [tr(row) for row in data if tr(row) is not None]
        self.stats.transformed = len(data)

        for ld in self.loaders:
            for row in data:
                try:
                    ld(row)
                    self.stats.loaded += 1
                except Exception:
                    self.stats.failed += 1

        self.stats.finished_at = datetime.utcnow().isoformat()
        return self.stats

    def stats_dict(self):
        return self.stats.__dict__

def csv_extractor(path):
    def _extract():
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))
    return _extract

def json_extractor(path):
    def _extract():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return _extract

def csv_loader(path):
    def _load(row):
        exists = Path(path).exists()
        with open(path, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if not exists:
                writer.writeheader()
            writer.writerow(row)
    return _load
