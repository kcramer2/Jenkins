#!/usr/bin/python
#		Python Submitter File
#		Kent Cramer II
#		In collaboration with Emile Tura ( pysendm[basis for mail function], mpi1.sub )
#		Edited: 10/17/2017
#
############################################################
#
#               Runs all submission test jobs 
#		Checks for known good output
# If output is bad,  and queue is empty  an alert email will be sent
#

# import OS for shell commands, and time for sleep function
import os, time, smtplib, subprocess

# Remove old test files
os.system("./clear.sh")

# creates the base submission commands for regular and dag submissions
command = "condor_submit"
command_dag = "condor_submit_dag jobdag.dag"
error = ''

# Create the list for each of the regular jobs to submit
tests = ('job1cpu.sub', 'jobDocker.sub', 'jobGluster.sub', 'jobMem.sub', 'mpi_run.sub', 'jobGpu.sub' )

# initializes the failure variable for exceptions.
failed_submit = 0

# create email function to call when sending alerts
# Derived from original pysendm.py By Emile Tura.
def send_email(error,text):
	# List of users to notify
	userList = ["turatsinze","kcramer3"]

	userNames = [u for u in userList]

	# Users email list
	#emailList = [name +  "@wisc.edu" for name in userNames]
	emailList = ["kcramer3@wisc.edu"]

	# Submit server running the script
	proc = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE, )
	submitserver = proc.communicate()[0]

	SERVER = "chtc.wisc.edu"
	FROM = "submit-test@chtc.wisc.edu"
	TO = emailList
	SUBJECT = ("issue with" + " " + submitserver)
	MSG = text + "\n" + error

	# Prepare actual message

	message = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (FROM, ", ".join(TO), SUBJECT, MSG)

	# Send the mail

	server = smtplib.SMTP(SERVER)
	server.sendmail(FROM, TO, message)
	server.quit()

def check_output(x):
        # This list will track which jobs do not have an out file yet.
        error = list()
        
        dir = os.popen("pwd").read()

	#Check for the existence of each output file, append error list for non-existing output files.
        if os.path.isfile(dir + "/cpu1.out") != True:
               error.append('cpu')
        if os.path.isfile(dir + "/gluster.mp4") != True and os.path.isfile(dir + "/gluster.out") != True:
               error.append('gluster')
        if os.path.isfile(dir + "/mpi.out") != True:
               error.append('mpi')
        if os.path.isfile(dir + "/jobGpu.out") != True:
               error.append('cpu')
        if os.path.isfile(dir + "/docker.out") != True:
               error.append('docker')
        if os.path.isfile(dir + "/jdag.out") != True:
               error.append('DAG')
        if os.path.isfile(dir + "/mem.out") != True and x != 'non-memory':
               error.append('memory')
	return error


# Loops through each job in the test list, creates a new command for the specific test.
for test in tests:
	run = command + " " + test

	# Attempts to run the new command variable
	return_val = os.system(run)
	if return_val != 0:
		failed = "echo 'job(s) failed to submit:' " + test + " >> submitter.log"
		os.system(failed)

		# Increments the failed_submit variable to prevent spam email from being sent from multiple failed submissions.
		failed_submit = 1

# checks to see if a submission failed.
if failed_submit == 1:
	# Email only once for any non-dag submissions errors.
	text = " One or more the non-dag jobs failed to submit. Please investigate"
	# opens the log file to pull failure messages
	log = open('submitter.log', 'r')
	# adds the text from submitter.log to the error variable to pass to send_email function
	error = log.read()
	send_email(error,text)
	log.close()
	# resets the failure messages
	failed_submit = 0

# Attempts to pass the command for the DAG job to the command line
return_val = os.system(command_dag)
# 'Handles' errors that occur with the dag submission command
if return_val != 0:
        failed_submit = 1
	failed = "echo 'job failed to submit: jobDAG' >> submitter.log"
        os.system(failed)

if failed_submit == 1:
	text = " The DAG job submission has failed to submit. Please investigate"
	log = open('submitter.log', 'r')
	error = log.read()
	send_email(error,text)
	log.close()
	failed_submit = 0


# Sets a variable to track how many loops have occured, tracking time in queue
elapsed = 0

# Main loop.
while True:
	# This set of commands checks for the Jobs in queue. If jobs have completed, this will be 0.
	# Rewritten with collaboration from Emile Tura.
	print('checking command - iter:' + str(elapsed))
	status = os.popen("condor_q | grep -i jobs | cut -c 1").read()
	status = status.rstrip()
	status = int(status)

	if status == 0:
		# no jobs are left in the queue, check for output, log the event, email if there are erros and  break loop
		errors = check_output('memory')
		if errors == []:
                        # logs the successful completion of the test
                        os.system("echo 'Submission/Completion of memory job: SUCCESS' >> submitter.log")
                        # break loop, all files are accounted for so jobs completed succesfully
                        break
		else:
                        # Outfile(s) not present, writting to log
                        os.system("echo 'Queued jobs 0. Completion of submitted jobs: FAILED(no output). Alerting via Email' >> submitter.log")
                        failed = ""
                        for i in errors:
                                failed = " -" + failed + i + "  "  
                        # Sends an email to inform of a failure during the submission checks
                        text = " These jobs left the queue but did not complete: " + "\n"
                        send_email(failed,text)

        elif elapsed >= 336:
		errors = check_output('memory')
		failed = 0
		for i in errors:
			if i == 'memory':
				failed = 1

                if failed == 0:
                        # logs the successful completion of the test
                        os.system("echo 'Completion of memory job: SUCCESS' >> submitter.log")
			# break while loop as this check is the maximum timeout for the Memory job / script
			break
                else:

                        # Outfile(s) not present, writting to log
                        os.system("echo 'Completion of Memory job: FAILED(no output). Alerting via Email' >> submitter.log")
                        failed = ""
                        for i in errors:
                                failed = " -" +  failed + i + "  "  
                        # Sends an email to inform of a failure during the submission checks
                        text = " The memory job did not complete, failed jobs: " + "\n"
                        send_email(failed,text)
			# break while loop, 7 days have passed and memory job has not completed
			break
	# checking the status and time elapsed variable. Time elapsed set for a 2 hour wait before alerting.
	elif elapsed == 4:
		errors = check_output('non-memory')
		if errors == []:
			# logs the successful completion of the test
			os.system("echo 'Submission/Completion of non-memory jobs: SUCCESS' >> submitter.log")

		else:
			# Outfile(s) not present, writting to log
			os.system("echo 'Completion of non-memory jobs: FAILED(missing output). Alerting via Email' >> submitter.log")
			failed = ""
			for i in errors:
				failed = " -" + failed + i + " "  
			# Sends an email to inform of a failure during the submission checks
			text = " The following tests have not completed running within 2 hours and may be stuck in the queue: " + "\n"
                        send_email(failed,text)
	else:
		print('failed check')
	# Increment the time elapsed variable and sleep for 10 minutes before checking again.
	print(elapsed)
	elapsed = elapsed + 1
	time.sleep(30)
