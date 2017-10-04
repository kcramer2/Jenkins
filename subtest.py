import os, time

# submit the test files when run

command = "condor_submit"
command_dag = "condor_submit_dag -f jobdag.dag"
tests = ('job1cpu.sub', 'jobDocker.sub', 'jobGluster.sub', 'jobMem.sub', 'mpi_run.sub', 'jobGpu.sub' )

for test in tests:
        run = command + " " + test
        try:
		print('Submitting: ' + test) 
		os.system(run)
        except:
                # Log output if job submission failed
                failed = "echo 'job(s) failed to submit:' " + test + " >> submitter.log"
                os.system(failed)
                # Send  email to notify of job submission failure
try:
        os.system(command_dag)
except:
        failed = "echo 'job failed to submit: jobDAG' >> submitter.log"
        os.system(failed)


