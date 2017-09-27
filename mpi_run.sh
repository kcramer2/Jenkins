#!/bin/bash

# Command to enable modules, and then load an appropriate MP/MPI module
. /etc/profile.d/modules.sh
module load openmpi-x86_64

#module load mpi/gcc/openmpi-1.6.4

# Command to run your OpenMP/MPI program
# (This example uses mpirun, other programs
# may use mpiexec, or other commands)

mpicc mpi1.c -o mpi1

mpirun -np 4 ./mpi1

