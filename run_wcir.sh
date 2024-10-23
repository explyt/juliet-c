#!/bin/bash

export LLVM_COMPILER=clang
export LLVM_CC_NAME=clang
export LLVM_CXX_NAME=clang++
export LLVM_COMPILER_PATH=~/clangir/build/bin

export WCIR_ERR_FILES=$(pwd)/wcir_err.log
export WCIR_COMPILED_FILES=$(pwd)/wcir_compiled.log

export LLVM_DISABLE_SYMBOLIZATION=1

cc=wcir cxx=wcir++ make

bear make
wcircc -j 4 build/compile_commands.json