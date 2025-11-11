from __future__ import annotations

import pathlib
import typing as t

import nox
from nox import options

options.default_venv_backend = "uv"
options.sessions = ["planck", "wien", "co2", "co2_absorption", "co2_schwingung"]
PYTHON_PATHS = [pathlib.Path(__file__).parent / "simulationen", "noxfile.py"]


# uv_sync taken from: https://github.com/hikari-py/hikari/blob/master/pipelines/nox.py#L48
#
# Copyright (c) 2020 Nekokatt
# Copyright (c) 2021-present davfsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
def uv_sync(
    session: nox.Session, /, *, include_self: bool = False, extras: t.Sequence[str] = (), groups: t.Sequence[str] = ()
) -> None:
    if extras and not include_self:
        raise RuntimeError("When specifying extras, set `include_self=True`.")

    args: list[str] = []
    for extra in extras:
        args.extend(("--extra", extra))

    group_flag = "--group" if include_self else "--only-group"
    for group in groups:
        args.extend((group_flag, group))

    session.run_install(
        "uv", "sync", "--frozen", *args, silent=True, env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location}
    )


@nox.session(reuse_venv=True)
def planck(session: nox.Session) -> None:
    uv_sync(session, groups=["planck"])

    session.run("python", "-m", "simulationen.planck")


@nox.session(reuse_venv=True)
def wien(session: nox.Session) -> None:
    uv_sync(session, groups=["planck"])

    session.run("python", "-m", "simulationen.wien")


@nox.session(reuse_venv=True)
def co2(session: nox.Session) -> None:
    uv_sync(session, groups=["co2"])

    session.run("python", "-m", "simulationen.co2_spektrum")
    session.run("python", "-m", "simulationen.co2_spektrum_under_1_5")
    session.run("python", "-m", "simulationen.co2_spektrum_v3_band")
    session.run("python", "-m", "simulationen.co2_spektrum_v2_band")


@nox.session(reuse_venv=True)
def co2_all(session: nox.Session) -> None:
    uv_sync(session, groups=["co2"])

    session.run("python", "-m", "simulationen.co2_spektrum")


@nox.session(reuse_venv=True)
def co2_small(session: nox.Session) -> None:
    uv_sync(session, groups=["co2"])

    session.run("python", "-m", "simulationen.co2_spektrum_under_1_5")


@nox.session(reuse_venv=True)
def co2_v3(session: nox.Session) -> None:
    uv_sync(session, groups=["co2"])

    session.run("python", "-m", "simulationen.co2_spektrum_v3_band")


@nox.session(reuse_venv=True)
def co2_v2(session: nox.Session) -> None:
    uv_sync(session, groups=["co2"])

    session.run("python", "-m", "simulationen.co2_spektrum_v2_band")


@nox.session(reuse_venv=True)
def co2_absorption(session: nox.Session) -> None:
    uv_sync(session, groups=["co2absorption"])

    session.run("python", "-m", "simulationen.co2_absorptionsgrad")


@nox.session(reuse_venv=True)
def co2_schwingung(session: nox.Session) -> None:
    uv_sync(session, groups=["co2"])

    session.run("python", "-m", "simulationen.co2_v2_schwingung")

@nox.session(reuse_venv=True)
def ruff(session: nox.Session) -> None:
    uv_sync(session, groups=["ruff"])

    session.run("python", "-m", "ruff", "format", *PYTHON_PATHS)
    session.run("python", "-m", "ruff", "check", *PYTHON_PATHS, "--select", "I", "--fix")
    session.run("python", "-m", "ruff", "check", *PYTHON_PATHS)
