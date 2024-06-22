from dataclasses import dataclass


@dataclass
class ArtifactMetadata:
    category: str
    content_identifier: str
    scrape_time_str: str
