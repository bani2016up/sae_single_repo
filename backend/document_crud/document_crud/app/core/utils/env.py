import os
from typing import NoReturn
from .path import BASE_ENV_TEMPLATE_PATH, STANDARD_ENV_LOC

def check_env() -> None | NoReturn:
    check_env_exists()
    check_env_matches_template(BASE_ENV_TEMPLATE_PATH)

def check_env_exists() -> None | NoReturn:
    env_path: str = os.getenv('ENV_PATH', STANDARD_ENV_LOC)
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Environment file '{env_path}' does not exist.")

def check_env_matches_template(template_path: str) -> None | NoReturn:
    env_path: str = os.getenv('ENV_PATH', STANDARD_ENV_LOC)

    def parse_env_file(file_path: str) -> dict:
        with open(file_path, 'r') as file:
            return dict(
                line.strip().split('=', 1) for line in file if line.strip() and not line.startswith('#')
            )

    template_vars: dict = parse_env_file(template_path)
    env_vars: dict = parse_env_file(env_path)

    missing_keys: list[str] = [key for key in template_vars if key not in env_vars]

    if missing_keys:
        raise ValueError(f"The following keys are missing in the environment file: {', '.join(missing_keys)}")


def create_env_from_template(template_path: str, output_path: str) -> None | NoReturn:
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    with open(output_path, 'w') as output_file:
        output_file.write(template_content)
