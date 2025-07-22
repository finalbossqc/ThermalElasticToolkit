#! /bin/bash

mpiexec -n $1 ../thermal-opt -i thermal.i --allow-unused --n-threads=$1
mkdir data
mv *.vtu data
mv *.pvtu data
