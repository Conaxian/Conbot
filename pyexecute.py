################################################################

import os
import time
import subprocess
import signal
import platform

import constants

################################################################

class PyExecute:

    def __init__(self, py_file, loc_dict, run_check_timeout=constants.run_check_timeout, exec_timeout=constants.exec_timeout, 
    module_whitelist=constants.module_whitelist, keyword_blacklist=constants.keyword_blacklist):

        self.loc_dict = loc_dict
        self.run_check_timeout = run_check_timeout
        self.exec_timeout = exec_timeout
        self.module_whitelist = module_whitelist
        self.keyword_blacklist = keyword_blacklist

        current_dir = os.path.dirname(__file__)
        current_path = os.path.abspath(current_dir)
        self.file_path = os.path.join(current_path, py_file)
        self.unix = platform.system() != "Windows"
        self.exec_time = 0

    def execute(self, code):

        output = self.run(code)
        return output

    def scan(self, code):

        lines = code.split("\n")
        for line in lines:

            # Check imports for dangerous modules
            if "import" in line:
                imported = line.replace("import", "").replace(" \n\t", "")
                modules = set(imported.split(","))
                if not modules.issubset(set(self.module_whitelist)):
                    return self.loc_dict["banned_module"]

            # Check code for banned keywords
            for keyword in self.keyword_blacklist:
                words = code.split(" ")
                words = [word.strip(".,;\\()[]{}_") for word in words]
                if keyword in words:
                    error = self.loc_dict["banned_keyword"]
                    return error.replace("$1", keyword)

    def is_running(self):

        if self.unix:
            tasklist_cmd = f"ps -p {self.pid}"
            tasklist_condition = "/0"
        else:
            tasklist_cmd = f'tasklist /FI "pid eq {self.pid}"'
            tasklist_condition = "INFO: No tasks are running"
        tasklist = os.popen(tasklist_cmd).read()
        if tasklist_condition in tasklist:
            return self.unix
        return not self.unix

    def run(self, code):

        self.exec_start = time.time()
        error = self.scan(code)
        if error:
            self.exec_time = time.time() - self.exec_start
            return error
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(code)

        python_cmd = "python3" if self.unix else "python"
        popen_args = [python_cmd, self.file_path]
        process = subprocess.Popen(popen_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        self.pid = process.pid

        limit = time.time() + self.exec_timeout
        while time.time() < limit:
            time.sleep(self.run_check_timeout)
            if not self.is_running():
                stdout, stderr = process.communicate()
                self.output = (stdout + b"\n" + stderr).decode("utf-8")
                self.exec_time = time.time() - self.exec_start
                return self.output

        kill_signal = signal.SIGTERM if self.unix else signal.CTRL_C_EVENT
        os.kill(self.pid, kill_signal)
        self.exec_time = time.time() - self.exec_start
        return self.loc_dict["timeout"]

################################################################
