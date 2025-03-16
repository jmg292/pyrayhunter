import json

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class QmdlManifestEntry:

    name: str
    start_time: str
    last_message_time: str
    qmdl_size_bytes: int
    analysis_size_bytes: int


@dataclass
class QmdlManifest:

    entries: List[QmdlManifestEntry]
    current_entry: Optional[QmdlManifestEntry]

    @staticmethod
    def from_dict(qmdl_manifest: dict):
        qmdl_manifest["entries"] = [QmdlManifestEntry(**x) for x in qmdl_manifest["entries"]]
        if qmdl_manifest["current_entry"] is not None:
            qmdl_manifest["current_entry"] = QmdlManifestEntry(**qmdl_manifest["current_entry"])
        return QmdlManifest(**qmdl_manifest)
