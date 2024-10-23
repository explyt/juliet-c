#!/usr/bin/python

import os
import fnmatch
import subprocess
import sys

from pathlib import Path

res_name = "result_juliet"

traverse_path = "testcases"
if len(sys.argv) > 1:
    traverse_path = sys.argv[1]

LLVM_COMPILER_PATH="LLVM_COMPILER_PATH"
compiler_path = os.getenv(LLVM_COMPILER_PATH)
if compiler_path is None:
    raise Exception(f"No {LLVM_COMPILER_PATH}")
opt_path = os.path.join(compiler_path, "cir-opt")

ws = 0
wscir = 0

compile_err = 0
compile_pass = 0


failed_paths = {}
c_all = 0
c_builds = 0
c_fails = 0

no_trace_paths = []

def process(path: str, failed_path: str):
    if failed_path in failed_paths:
        failed_paths[failed_path].append(path)
    else:
        failed_paths[failed_path] = [path]

for root, dir, files in os.walk(traverse_path):
    for item in files:
        # e_path = root + "/" + Path(Path(Path(item).stem).stem).stem[1:]
        # if(not Path(e_path + ".cpp").is_file()):
        #     e_path += ".cpp"
        #     continue
        # if(not Path(e_path + ".c").is_file()):
        #     e_path += ".c"
        #     continue

        e_path = item

        if item.endswith(".s"):
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
            
            c_all += 1
            c_builds += 1
        elif item.endswith(".err"):
            path = root + "/" + item
            path_err_r = open(path, "r+")

            for line in path_err_r:
                failed_path = ""
                if(line.find("Assertion `") != -1) :
                    failed_path = line.split(" ")[1][:-1]
                elif(line.startswith("UNREACHABLE executed at")):
                    failed_path = line.split(" ")[-1][:-2]
                elif(line.startswith("fatal error: error in backend: CIR codegen: module verification")):
                    failed_path = "fatal error: error in backend: CIR codegen: module verification"
                else:
                    continue
                process(e_path, failed_path)
                break

            else:
                no_trace_paths.append(e_path)
                # print("Error without stacktrace for file:", path)

            path_err_r.close()

            c_all += 1
            c_fails += 1
            




print(f"All: {c_all}")
print(f"Builded:", c_builds)
print(f"Failed: {c_fails}")
print(f"Unique errors: {len(failed_paths)}")
print(f"No trace: {len(no_trace_paths)}")
print()

print(f"Text: {ws} Byte")
print(f"Binary: {wscir} Byte")
print(f"Compiled to binary: {compile_pass}")
print(f"Failed compile to binary: {compile_err}")
print()

print(f"Results in: {res_name}.txt {res_name}_short.txt")

results = open(res_name + ".txt", "w+")
results_short = open(res_name + "_short.txt", "w+")

results.write("All: " + str(c_all) + "\n")
results.write("Failed: " + str(c_fails) + "\n")
results.write("Unique errors:" + str(len(failed_paths)))
results.write("\n")

results.write("No trace " + str(len(no_trace_paths)) + "\n")
results_short.write("No trace " + str(len(no_trace_paths)) + "\n")
for path in no_trace_paths:
    results.write(path + "\n")
results.write("\n")

for failed_path, paths in failed_paths.items():
    results.write(failed_path + " " + str(len(paths)) + "\n")
    results_short.write(failed_path + " " + str(len(paths)) + "\n")
    for path in paths:
        results.write(path + "\n")
    results.write("\n")


results.close()
results_short.close()