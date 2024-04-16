from osparc_client import StudiesApi as _StudiesApi

from ._utils import dev_feature


class StudiesApi(_StudiesApi):
    """Class for interacting with solvers"""

    @dev_feature
    def clone_study(self, study_id, **kwargs):
        return super(StudiesApi, self).clone_study(study_id=study_id, **kwargs)

    @dev_feature
    def create_study_job(self, study_id, job_inputs, **kwargs):
        return super(StudiesApi, self).create_study_job(
            study_id=study_id, job_inputs=job_inputs, **kwargs
        )

    @dev_feature
    def delete_study_job(self, study_id, job_id, **kwargs):
        return super(StudiesApi, self).delete_study_job(
            study_id=study_id, job_id=job_id, **kwargs
        )

    @dev_feature
    def get_study(self, study_id, **kwargs):
        return super(StudiesApi, self).get_study(study_id=study_id, **kwargs)

    @dev_feature
    def get_study_job(self, study_id, job_id, **kwargs):
        return super(StudiesApi, self).get_study_job(
            study_id=study_id, job_id=job_id, **kwargs
        )

    @dev_feature
    def inspect_study_job(self, study_id, job_id, **kwargs):
        return super(StudiesApi, self).inspect_study_job(
            study_id=study_id, job_id=job_id, **kwargs
        )

    @dev_feature
    def list_studies(self, **kwargs):
        return super(StudiesApi, self).list_studies(**kwargs)

    @dev_feature
    def list_study_jobs(self, study_id, **kwargs):
        return super(StudiesApi, self).list_study_jobs(study_id=study_id, **kwargs)

    @dev_feature
    def list_study_ports(self, study_id, **kwargs):
        return super(StudiesApi, self).list_study_ports(study_id=study_id, **kwargs)

    @dev_feature
    def replace_study_job_custom_metadata(
        self, study_id, job_id, job_metadata_update, **kwargs
    ):
        return super(StudiesApi, self).list_study_ports(
            study_id=study_id,
            job_id=job_id,
            job_metadata_update=job_metadata_update,
            **kwargs
        )

    @dev_feature
    def start_study_job(self, study_id, job_id, **kwargs):
        return super(StudiesApi, self).start_study_job(
            study_id=study_id, job_id=job_id, **kwargs
        )

    @dev_feature
    def stop_study_job(self, study_id, job_id, **kwargs):
        return super(StudiesApi, self).start_study_job(
            study_id=study_id, job_id=job_id, **kwargs
        )
