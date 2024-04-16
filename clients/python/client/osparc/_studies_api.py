from typing import Any

from osparc_client import StudiesApi as _StudiesApi

from ._utils import dev_features_enabled


class StudiesApi(_StudiesApi):
    """Class for interacting with solvers"""

    _dev_features = [
        "clone_study",
        "create_study_job",
        "delete_study_job",
        "get_study",
        "get_study_job",
        "inspect_study_job",
        "list_studies",
        "list_study_jobs",
        "list_study_ports",
        "replace_study_job_custom_metadata",
        "start_study_job",
        "stop_study_job",
    ]

    def __getattribute__(self, name: str) -> Any:
        if (name in StudiesApi._dev_features) and (not dev_features_enabled()):
            raise NotImplementedError(f"StudiesApi.{name} is still under development")
        return super().__getattribute__(name)
