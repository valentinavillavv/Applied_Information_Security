##########################################################################
#                       Helper functions                                 #
##########################################################################
import datetime
import subprocess

def execute_command(command):
    log_execution(current_time() + '\t' + 'Command from client: ' +  command)
    executed = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Successful execution
    if executed.returncode == 0:
        log_execution(current_time() + '\t' + 'Returned value: ' + executed.stdout)
        return 'Returned value: ' + executed.stdout
    
    # Error occured during execution
    log_execution(current_time() + '\t' + 'Error: ' + executed.stderr)
    return 'Error: ' + executed.stderr

# Log server data to log
def log_execution(log_output):
    with open('./log/server.log', 'a') as log:
        log.write(log_output+'\n')

# Return current time
def current_time():
    return str(datetime.datetime.now())