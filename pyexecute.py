################################################################

import os
import time
import subprocess
import signal
import platform

import const

################################################################

kw_delimiters = [" ", "\n", "\t", ".", ",", ":", ";", "\\", "=", "+", "-", "*", "/", "%", "@", "(", ")", "[", "]", "{", "}"]
kw_delimiters_str = "".join(kw_delimiters)

################################################################

class PyExecute:

    def __init__(self, py_file, loc_dict, run_check_timeout=const.run_check_timeout, exec_timeout=const.exec_timeout, 
    module_whitelist=const.module_whitelist, keyword_blacklist=const.keyword_blacklist):

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
        kw_code = code
        for delimiter in kw_delimiters:
            kw_code = kw_code.replace(delimiter, ".")
        words = kw_code.split(".")
        words = [word.strip(kw_delimiters_str) for word in words]

        # Check imports for dangerous modules
        for line in lines:
            if "import" in line:
                imported = line.replace("import", "").replace(" \n\t", "")
                modules = set(imported.split(","))
                if not modules.issubset(set(self.module_whitelist)):
                    return self.loc_dict["banned_module"]

        # Check code for banned keywords
        for keyword in self.keyword_blacklist:
            if keyword in words:
                error = self.loc_dict["banned_keyword"]
                return error.replace("$1", keyword)

    def is_running(self):

        if self.unix:
            tasklist_cmd = f"ps -p {self.pid}"
            tasklist_condition = "<defunct>"
        else:
            tasklist_cmd = f'tasklist /FI "pid eq {self.pid}"'
            tasklist_condition = "INFO: No tasks are running"
        tasklist = os.popen(tasklist_cmd).read()
        return tasklist_condition not in tasklist

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
        if self.unix:
            process = subprocess.Popen(popen_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(popen_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW)
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
