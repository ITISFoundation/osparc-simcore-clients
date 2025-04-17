from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import osparc
import asyncio
from tempfile import TemporaryDirectory


class OsparcUser(BaseSettings):
    host: str = Field(default=...)
    key: str = Field(default=...)
    secret: str = Field(default=...)
    model_config = SettingsConfigDict(env_prefix="osparc_api_")


def osparc_client():
    user = OsparcUser()
    config = osparc.Configuration(
        host=user.host, username=user.key, password=user.secret
    )
    return osparc.ApiClient(config)


def check_credentials():
    with osparc_client() as api_client:
        user_api = osparc.UsersApi(api_client)
        profile = user_api.get_my_profile()
        print(profile.model_dump_json(indent=2))


async def run(program_key: str, version: str):
    with osparc_client() as api_client:
        files_api = osparc.FilesApi(api_client)
        programs_api = osparc.ProgramsApi(api_client)
        # check if the program exists
        program = programs_api.get_program_release(
            program_key=program_key, version=version
        )

        program_job = programs_api.create_program_job(
            program_key=program.id, version=program.version
        )
        print(program_job.model_dump_json(indent=2))

        with TemporaryDirectory() as tmp_dir:
            # Upload the input file
            tmp_file = Path(tmp_dir) / "tmpfile"
            tmp_file.write_text("Hi oSPARC 👋")
            await files_api.upload_file_to_program_job_async(
                file=tmp_file,
                program_key=program.id,
                program_version=program.version,
                job_id=program_job.id,
                workspace_path="workspace/tmpdirectory/tmpfile",
            )


if __name__ == "__main__":
    check_credentials()
    asyncio.run(
        run(program_key="simcore/services/dynamic/jupyter-math", version="3.0.2")
    )
