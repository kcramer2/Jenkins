#
#		Python Submitter File
#		Kent Cramer II
#		10/2/2017
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
		failed-submit = 1
if failed-submit == 1:
	# Email only once for any non-dag submissions errors. A seperate email template should be utlized
	email_comm = "pysendm.py" 

try:
	os.system(command_dag)
except:
        failed = "echo 'job failed to submit: jobDAG' >> submitter.log"
        os.system(failed)


elapsed = 0
while True:
	# The following outfiles are checked for their existence:
	# cpu1.out, gluster.mov, mpi.out, jobGpu.out, docker.out, mem.out, jdag.out
	# The presence of these files should indicate successful completeion of the submission jobs
	# This loop will check every 10 minutes for the status of these jobs, if 2 hours pass an alert will be generated

	# This list will track which jobs do not have an out file yet.
	error = list()

	# This set of commands checks for the Jobs in queue. If jobs have not yet been processed, this will not be 0.
	print('checking command - iter:' + str(elapsed))
	status = os.popen("condor_q | grep -i jobs | cut -c 1").read()
	status = status.rstrip()
	status = int(status)

	# checking the status and time elapsed variable. Time elapsed set for a 2 hour wait before alerting.
	if status == 0 or elapsed >= 10:
		# Begin Checking output files, adds jobs without an out file to the error list.
		print('if statement 1')
		print(error)
		if os.path.isfile("/path/to/cpu1.out") != True:
			error.append('cpu')
	        if os.path.isfile("/home/kcramer/gluster.mov") != True and os.path.isfile("/path/to/gluser.out") != True:
	                error.append('gluster')
	        if os.path.isfile("/home/kcramer/mpi.out") != True:
	                error.append('mpi')
	        if os.path.isfile("/home/kcramer/jobGpu.out") != True:
	                error.append('cpu')
	        if os.path.isfile("/home/kcramer/docker.out") != True:
	                error.append('docker')
	        if os.path.isfile("/home/kcramer/mem.out") != True:
	                error.append('memory')
	        if os.path.isfile("/home/kcramer/jdag.out") != True:
	                error.append('DAG')
		print('this should hold strings', error)
		if error == []:
			os.system("echo 'Submission/Completion of jobs: SUCCESS' >> submitter.log")
			break
		else:
			os.system("echo 'Completion of jobs: FAILED. Alerting via Email' >> submitter.log")
			#email_comm = "pysendm.py " + error
			#os.system(email_comm)
			break
	else:
		print('failed check')
	# Increment the time elapsed variable and sleep for 10 minutes before checking again.
	print(elapsed)
	elapsed = elapsed + 1
	time.sleep(6)
