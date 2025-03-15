from dataclasses import dataclass, field
from datetime import datetime as DateTime, timezone as TimeZone


@dataclass
class ArtifactMetadata:
    category: str
    content_identifier: str
    datetime: DateTime = field(
        default_factory=lambda: DateTime.now(TimeZone.utc), init=False
    )
