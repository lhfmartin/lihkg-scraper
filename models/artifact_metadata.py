from dataclasses import dataclass, field
from datetime import datetime as DateTime, timezone as TimeZone
from typing import ClassVar, Self
from enums import ArtifactCategory


@dataclass
class ArtifactMetadata:
    category: ArtifactCategory
    content_identifier: str
    datetime: DateTime = field(
        default_factory=lambda: DateTime.now(TimeZone.utc), init=False
    )
    DATE_TIME_STR_FORMAT: ClassVar[str] = "%Y%m%dT%H%M%SZ"

    @classmethod
    def from_folder_name(cls, folder_name: str) -> Self:
        artifact_metadata = ArtifactMetadata(
            ArtifactCategory(folder_name.split("_")[0]),
            folder_name.split("_", 1)[1].rsplit("_", 1)[0],
        )
        artifact_metadata.datetime = DateTime.strptime(
            folder_name.split("_")[-1], cls.DATE_TIME_STR_FORMAT
        )
        return artifact_metadata
