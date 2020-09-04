import subprocess
working_directory = "/home/can/workspace/arrc_server"
p = subprocess.Popen(["python3", "arrc_server.py"], cwd=working_directory)
p.wait()