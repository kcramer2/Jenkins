import os, time

# submit the test files when run

elapsed = 0
while true:
	# The following outfiles are checked for their existence:
	# cpu1.out, gluster.mov, mpi.out, jobGpu.out, docker.out, mem.out, jdag.out
	# The presence of these files should indicate successful completeion of the submission jobs
	# This loop will check every 10 minutes for the status of these jobs, if 2 hours pass an alert will be generated

	# This list will track which jobs do not have an out file yet.
	error = list()

	# This set of commands checks for the Jobs in queue. If jobs have not yet been processed, this will not be 0.
	status = os.popen("condor_q | grep -i jobs | cut -c 1").read()
	status = status.rstrip()

	# checking the status and time elapsed variable. Time elapsed set for a 2 hour wait before alerting.
	if status == 0 or elapsed >= 12:
		# Begin Checking output files, adds jobs without an out file to the error list.
		if os.path.isfile("/path/to/cpu1.out") == true:
			continue
		else:
			error.append('cpu')
	        if os.path.isfile("/home/kcramer/gluster.mov") == true && os.path.isfile("/path/to/gluser.out") == true:
	                continue
	        else:
	                error.append('gluster')
	        if os.path.isfile("/home/kcramer/mpi.out") == true:
	                continue
	        else:
	                error.append('mpi')
	        if os.path.isfile("/home/kcramer/jobGpu.out") == true:
	                continue
	        else:
	                error.append('cpu')
	        if os.path.isfile("/home/kcramer/docker.out") == true:
	                continue
	        else:
	                error.append('docker')
	        if os.path.isfile("/home/kcramer/mem.out") == true:
	                continue
	        else:
	                error.append('memory')
	        if os.path.isfile("/home/kcramer/jdag.out") == true:
	                continue
	        else:
	                error.append('DAG')
		if error == "":
			os.system("echo 'Submission/Completion of jobs: SUCCESS' >> submitter.log")
			break
		else:
			os.system("echo 'Completion of jobs: FAILED. Alerting via Email' >> submitter.log")
			#email_comm = "pysendm.py " + error
			#os.system(email_comm)
			break

	# Increment the time elapsed variable and sleep for 10 minutes before checking again.
	elapsed = elapsed + 1
	time.sleep(600)


