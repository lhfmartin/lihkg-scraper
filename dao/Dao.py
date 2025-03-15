import os
import pathlib

from models import ArtifactMetadata


class Dao:
    def __init__(self, output_folder_path: str, artifact_metadata: ArtifactMetadata):
        self.artifact_folder_path = os.path.join(
            output_folder_path,
            f"{artifact_metadata.category}_{artifact_metadata.content_identifier}_{artifact_metadata.datetime.strftime(ArtifactMetadata.DATE_TIME_STR_FORMAT)}",
        )
        pathlib.Path(self.artifact_folder_path).mkdir(parents=True, exist_ok=True)
