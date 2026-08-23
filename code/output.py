"""Copy runtime AWS values from `terraform output -json` into .env.local.

The Terraform state is never read back here; the Makefile dumps
`terraform output -json` to output.json first (see `make infra-prep`).
"""

import json

from envutil import update_env_file

ENV_LOCAL = ".env.local"


def main() -> None:
    with open("output.json") as json_file:
        json_data = json.load(json_file)

    update_env_file(ENV_LOCAL, "DBS_ENDPOINT", json_data["DBS_ENDPOINT"]["value"])
    update_env_file(ENV_LOCAL, "AWS_DB_ML", json_data["AWS_DB_ML"]["value"][:-5])
    update_env_file(
        ENV_LOCAL, "AWS_DB_MONITOR", json_data["AWS_DB_MONITOR"]["value"][:-5]
    )
    print(f"Wrote DBS_ENDPOINT, AWS_DB_ML, AWS_DB_MONITOR to {ENV_LOCAL}")


if __name__ == "__main__":
    main()
