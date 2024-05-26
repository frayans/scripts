#!/usr/bin/python3
# arkaive.py
# a basic and configurable auto-archiver.
# config format:
# [<archive_name>]
# input = "" <- the path to a directory
# output = "" <- where the archive will be placed

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from shutil import make_archive
from tomllib import load as tomload
from typing import Iterator

from platformdirs import user_config_dir, user_log_dir

APP_NAME = "arkaive"
VERSION = "0.1.0"
CONFIG_FILE = "config.toml"
LOGGER = logging.getLogger(APP_NAME)


class Format(StrEnum):
    GZIP = ("gztar",)
    BZIP2 = "bztar"
    LZMA = "xztar"


@dataclass
class Archive:
    name: str
    input: Path
    output: Path


def create_archive(archive: Archive, format: Format) -> None:
    LOGGER.info(
        f"Creating archive `{archive.name}` at {archive.output} from {archive.input}"
    )
    try:
        make_archive(
            archive.output / archive.name, format, archive.input, "", logger=LOGGER
        )
    except Exception as e:
        LOGGER.error(e)


def read_config(path: Path) -> Iterator[Archive]:
    try:
        with path.open("rb") as conf:
            data = tomload(conf)
            for k, v in data.items():
                archive = Archive(
                    k, Path(v["input"]).expanduser(), Path(v["output"]).expanduser()
                )
                yield archive
    except Exception as e:
        LOGGER.error(e)


def main() -> None:
    logging.basicConfig(
        filename=f"{user_log_dir(APP_NAME)}/{APP_NAME}-{datetime.now()}.log"
    )
    LOGGER.info("Getting configs...")
    config_path = Path(user_config_dir(APP_NAME)) / CONFIG_FILE
    for archive in read_config(config_path):
        create_archive(archive, Format.GZIP)
    LOGGER.info("Finished.")


if __name__ == "__main__":
    main()
