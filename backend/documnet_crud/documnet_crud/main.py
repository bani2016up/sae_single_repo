import traceback
from app.core.utils.env import check_env, create_env_from_template, BASE_ENV_TEMPLATE_PATH, STANDARD_ENV_LOC

if __name__ == "__main__":
    try:
        check_env()
    except FileNotFoundError as _:
        traceback.print_exc()
        create_env_from_template(BASE_ENV_TEMPLATE_PATH, STANDARD_ENV_LOC)
        print(f"Environment file '{STANDARD_ENV_LOC}' created from template '{BASE_ENV_TEMPLATE_PATH}'.")
    except ValueError as _:
        traceback.print_exc()
    else:
        import uvicorn
        uvicorn.run("app.core.app:app", host="0.0.0.0", port=8000, reload=True)
