"""
Extract PS4 .pkg DLC/addons

29/08/2026
"""

import os
import re
import shutil
import subprocess

# Folder containing the DLC files
input_folder = input("Path to directory containing .pkg files: ")
temp_folder = os.path.join(input_folder, "DLC_temp")

for pkg in os.listdir(input_folder):
    if not pkg.lower().endswith(".pkg"):
        continue

    print(pkg + " extracting...")
    pkg_path = os.path.join(input_folder, pkg)

    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)

    subprocess.run(["PkgTool", "pkg_makegp4", pkg_path, temp_folder], check=True)

    os.remove(os.path.join(temp_folder, "Project.gp4"))

    param_sfo = os.path.join(temp_folder, "sce_sys", "param.sfo")

    result = subprocess.run(
        ["PkgTool", "sfo_listentries", param_sfo],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    output = result.stdout.decode("utf-8", errors="ignore")

    match = re.search(rb"CONTENT_ID.*?_00-(\S+)", result.stdout)

    content_id = match.group(1).decode("ascii")

    output_folder = os.path.join(input_folder, content_id)

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    shutil.copytree(temp_folder, output_folder)

    shutil.rmtree(temp_folder)
    print(pkg + " complete.")

print("Done.")
