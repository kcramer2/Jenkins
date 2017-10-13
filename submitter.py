#
#		Python Submitter File
#		Kent Cramer II
#		Edited: 10/13/2017
#
############################################################
#
#               Runs all submission test jobs 
#		Checks for known good output
# If output is bad,  and queue is empty  an alert email will be sent
#

# import OS for shell commands, and time for sleep function
import os, time, smtplib, subprocess

# creates the base submission commands for regular and dag submissions
command = "condor_submit"
command_dag = "condor_submit_dag jobdag.dag"

# Create the list for each of the regular jobs to submit
tests = ('job1cpu.sub', 'jobDocker.sub', 'jobGluster.sub', 'jobMem.sub', 'mpi_run.sub', 'jobGpu.sub' )

# initializes the failure variable for exceptions.
failed_submit = 0

# create email function to call when sending alerts
def send_email(error,text):
	# List of users to notify
	userList = ["turatsinze","kcramer3"]

	userNames = [u for u in userList]

	# Users email list
	emailList = [name +  "@wisc.edu" for name in userNames]


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




# Loops through each job in the test list, creates a new command for the specific test.
for test in tests:
	run = command + " " + test

	# Attempts to run the new command variable
	try:
		os.system(run)

	# 'handles' the exceptions if the command fails
	except:
		# Log output if job submission failed
		failed = "echo 'job(s) failed to submit:' " + test + " >> submitter.log"
		os.system(failed)

		# Increments the failed_submit variable to prevent spam email from being sent from multiple exceptions.
		failed_submit = 1

# checks to see if an exception was encountered
if failed_submit == 1:
	# Email only once for any non-dag submissions errors. A seperate email template should be utlized
	text = " One or more the non-dag jobs failed to submit. Please investigate"
	send_mail(error,text)
	failed_submit = 0

# Attempts to pass the command for the DAG job to the command line
try:
	os.system(command_dag)
# 'Handles' errors that occur with the dag submission command
except:
        failed_submit = 1
	failed = "echo 'job failed to submit: jobDAG' >> submitter.log"
        os.system(failed)

if failed_submit == 1:
	text = " The DAG job submission has failed to submit. Please investigate"
	send_mail(error,text)
	failed_submit = 0


# Sets a variable to track how many loops have occured to track time in queue
elapsed = 0

# Main loop.
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
	if status == 0 or elapsed >= 12:
		# Begin Checking output files, adds jobs without an out file to the error list.
		print('if statement 1')
		print(error)
		if os.path.isfile("/path/to/cpu1.out") != True:
			error.append('cpu')
	        if os.path.isfile("/home/kcramer/gluster.mp4") != True and os.path.isfile("/home/kcramer/gluster.out") != True:
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

		# checks for an empty list, indicating all output files are present
		if error == []:

			# logs the successful completion of the test
			os.system("echo 'Submission/Completion of jobs: SUCCESS' >> submitter.log")

			# exits the loop
			break
		else:

			# Outfile(s) not present, writting to log
			os.system("echo 'Completion of jobs: FAILED. Alerting via Email' >> submitter.log")

			# Sends an email to inform of a failure during the submission checks
			text = " The following tests have not completed running within 2 hours and may be stuck in the queue" + "\n"
			send_email(error,test)
			break
	else:
		print('failed check')
	# Increment the time elapsed variable and sleep for 10 minutes before checking again.
	print(elapsed)
	elapsed = elapsed + 1
	time.sleep(6)
