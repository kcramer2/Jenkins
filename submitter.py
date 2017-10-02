#
#		Python Submitter File
#		Kent Cramer II
#		9/22/2017
#
############################################################
#
#               Runs all submission test jobs 
#		Checks for known good output
# If output is bad,  and queue is empty  an alert email will be sent
#

import os, time

# submit the test files when run

command = "condor_submit"
command_dag = "condor_submit_dag jobdag.dag"
tests = ('job1cpu.sub', 'jobDocker.sub', 'jobGluster.sub', 'jobMem.sub', 'mpi_run.sub', 'jobGpu.sub' )

for test in tests:
	run = command + " " + test
	try:
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

elapsed = 0
while true:
	# The following outfiles are checked for their existence:
	# cpu1.out, gluster.mov, mpi.out, jobGpu.out, docker.out, mem.out, jdag.out
	# The presence of these files should indicate successful completeion of the submition
	# This loop will check every 10 minutes for the status of these jobs, if 2 hours pass an alert will be generated

	# This list will track with jobs do not have an out file yet.
	error = list()

	# This set of commands checks for the Jobs in queue. If jobs have not yet been processed, this will no be 0.
	status_com = "condor_q | grep -i total | cut -c 1"
	status = os.system(status_com)
	if status != 0:	
		# Begin Checking out files if there are no more jobs in the queue.
		if os.path.isfile("/path/to/cpu1.out") == true:
			continue
		else:
			error.append('cpu')
	        if os.path.isfile("/path/to/gluster.mov") == true && os.path.isfile("/path/to/gluser.out") == true:
	                continue
	        else:
	                error.append('gluster')
	        if os.path.isfile("/path/to/mpi.out") == true:
	                continue
	        else:
	                error.append('mpi')
	        if os.path.isfile("/path/to/jobGpu.out") == true:
	                continue
	        else:
	                error.append('cpu')
	        if os.path.isfile("/path/to/docker.out") == true:
	                continue
	        else:
	                error.append('docker')
	        if os.path.isfile("/path/to/mem.out") == true:
	                continue
	        else:
	                error.append('memory')
	        if os.path.isfile("/path/to/jdag.out.out") == true:
	                continue
	        else:
	                error.append('DAG')
	# checking the time elapsed variable, this is set for a 2 hour wait for job completion before alerting.
	if elapsed < 12:
		continue
	else:
		# send email template.
		# Jobs are still in the queue after 2 hours and should have completed.

	# Increment the time elapsed variable and sleep for 10 minutes before checking again.
	elapsed = elapsed + 1
	time.sleep(600)




