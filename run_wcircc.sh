#!/bin/bash

export LLVM_COMPILER=clang
export LLVM_CC_NAME=clang
export LLVM_CXX_NAME=clang++

export WCIR_ERR_FILES=$(pwd)/wcir_err.log
export WCIR_COMPILED_FILES=$(pwd)/wcir_compiled.log

export LLVM_DISABLE_SYMBOLIZATION=1


TESTCASE=.

if [ $# -eq 1 ]
  then
    TESTCASE=$1
fi


#TODO maybe add this to wcircc
rm $WCIR_ERR_FILES
rm $WCIR_COMPILED_FILES

bear -- make -j8 -B -C $TESTCASE
wcircc -j 8 compile_commands.json

# cc=wcir cxx=wcir++ make -B -C testcases/CWE121_Stack_Based_Buffer_Overflow/s02

./collect_wcir_results.py $TESTCASE