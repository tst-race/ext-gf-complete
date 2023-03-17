#!/usr/bin/env python3

#
# Copyright 2023 Two Six Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Script to build GF-Complete for RACE
"""

import logging
import os
import race_ext_builder as builder


def get_cli_arguments():
    """Parse command-line arguments to the script"""
    parser = builder.get_arg_parser("gf-complete", "1.0.3", 1, __file__)
    return builder.normalize_args(parser.parse_args())


if __name__ == "__main__":
    args = get_cli_arguments()
    builder.make_dirs(args)
    builder.setup_logger(args)

    builder.install_packages(args, [
        "automake=1:1.16.1*",
        "libtool=2.4.6*",
    ])

    # This commit is the latest on the master branch as of 2017-04-10
    ref = "a6862d10c9db467148f20eef2c6445ac9afd94d8"

    builder.fetch_source(
        args=args,
        source=f"https://github.com/ceph/gf-complete/archive/{ref}.tar.gz",
        extract="tar.gz",
    )

    source_dir = os.path.join(args.source_dir, f"gf-complete-{ref}")
    env = builder.create_standard_envvars(args)

    logging.root.info("Configuring build")
    if args.target.startswith("android"):
        builder.execute(args, [
            "autoreconf",
            "--install",
        ], cwd=source_dir, env=env)

        target = "x86_64-linux-android" if "x86" in args.target else "aarch64-linux-android"
        builder.execute(args, [
            "./configure",
            "--prefix=/",
            f"--host={target}",
            f"--target={target}"
        ], cwd=source_dir, env=env)

    else:
        builder.execute(args, [
            "autoreconf",
            "--install",
        ], cwd=source_dir, env=env)

        target = "x86_64-linux-gnu" if "x86" in args.target else "aarch64-linux-gnu"
        builder.execute(args, [
            "./configure",
            "--prefix=/",
            f"--host={target}",
            f"--target={target}"
        ], cwd=source_dir, env=env)

    logging.root.info("Building")
    builder.execute(args, [
        "make",
        "-j",
        args.num_threads,
    ], cwd=source_dir, env=env)
    builder.execute(args, [
        "make",
        f"DESTDIR={args.install_dir}",
        "install",
    ], cwd=source_dir, env=env)

    builder.create_package(args)
