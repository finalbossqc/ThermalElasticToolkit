#! /bin/bash

mpiexec -n $1 ../thermal-opt -i thermal.i --allow-unused
mkdir data
mv *.vtu data
mv *.pvtu data
