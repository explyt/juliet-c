#!/usr/bin/python

import os
import fnmatch
import subprocess

from pathlib import Path

traverse_path = "testcases"

LLVM_COMPILER_PATH="LLVM_COMPILER_PATH"
compiler_path = os.getenv(LLVM_COMPILER_PATH)
if compiler_path is None:
    raise Exception(f"No {LLVM_COMPILER_PATH}")
opt_path = os.path.join(compiler_path, "cir-opt")

ws = 0
wscir = 0

i = 0
compile_err = 0
compile_pass = 0

for root, dir, files in os.walk(traverse_path):
    for item in files:
        if item.endswith(".s"):
            if(i % 1000 == 0):
                print("temp:", i, ws, wscir)
            path = root + "/" + item
            path_cir = path + "cir"
            cir_file = open(path_cir, "w")
            run_command = [opt_path] + ["--emit-bytecode"] + [path]

            try:
                subprocess.check_call(run_command, stdout=cir_file)
                wscir += os.path.getsize(path_cir)
                ws += os.path.getsize(path)
                compile_pass += 1
            except subprocess.CalledProcessError as err:
                compile_err += 1
                print(err)
            i += 1

print("Text: ", ws)
print("Binary: ", wscir)
print("Pass: ", compile_pass)
print("Failed: ", compile_err)