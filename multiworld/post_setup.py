# Copyright 2024 Cisco Systems, Inc. and its affiliates
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
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
import pathlib
import shutil
import site


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("patchfile")
    args = parser.parse_args()

    patch_basename = os.path.basename(args.patchfile)

    path_to_sitepackages = site.getsitepackages()[0]

    dst = os.path.join(path_to_sitepackages, patch_basename)
    shutil.copyfile(args.patchfile, dst)

    os.chdir(path_to_sitepackages)

    os.system(f"patch -p1 < {patch_basename}")
    p = pathlib.Path(patch_basename)
    p.unlink()

    files_to_copy = ["world_manager.py", "world_communicator.py"]
    for f in files_to_copy:
        src = os.path.join(path_to_sitepackages, "multiworld", f)
        dst = os.path.join(path_to_sitepackages, "torch/distributed", f)
        shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
