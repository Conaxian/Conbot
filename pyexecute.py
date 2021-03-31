class PyExecute:

    def __init__(self, exec_file, loc):

        self.__run__ = self.__execute_main__(exec_file, loc)
        self.exec_time = 0

    def execute(self, code=None):
        
        output = self.__run__.run_code(code)
        self.exec_time = output[1]
        return output[0]

    def is_safe(self, code=None):

        return self.__run__.is_safe(code)
    
    class __execute_main__:

        def __init__(self, exec_file, loc):

            import time
            import os
            import subprocess
            import threading
            import signal

            current_dir = os.path.dirname(__file__)
            current_path = os.path.abspath(current_dir)
            self.local_dir = current_path.replace("\\", "/")
            self.timeout_worker = 5
            self.check_script_timeout = 0.1

            self.time = time
            self.os = os
            self.subprocess = subprocess
            self.threading = threading
            self.signal = signal

            self.output = None
            self.execute_filename = exec_file

            self.error_timeout = loc["err_exec_timeout"].replace("$1", str(self.timeout_worker))
            self.error_untrusted_module = loc["err_exec_banned_module"]
            self.error_dangerous_keyword = loc["err_exec_banned_keyword"]

            self.trust_modules = ["datetime", "math", "random", "hashlib", "time", "getpass", "socket", "urllib"]
            self.dangerous_keywords = ["input", "exec", "eval", "compile", "open", "builtins", "os", "globals", "locals", "breakpoint", "dir", "delattr", "getattr", "repr", "vars"]
            self.encoding = "ISO-8859-1"

            self.remove_last_char = lambda x: [x[:len(x)-3] if x[len(x)-3:] == "\r\n\n" else x][0]

        def worker(self, do_return=False):

            self.output = None
            popen_args = ["python3", self.execute_filename]
            if not do_return:
                process = self.subprocess.Popen(popen_args, stdout=self.subprocess.DEVNULL, stderr=self.subprocess.STDOUT)
                self.pid = process.pid
            else:
                process = self.subprocess.Popen(popen_args, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
                self.pid = process.pid
                stdout, stderr = process.communicate()
                self.exec_time = self.time.time() - self.execute_start
                output = (stdout + b"\n" + stderr)
                output = output.decode(self.encoding)
                output = self.remove_last_char(output)
                return [output, self.exec_time]
        
        def check_if_running(self):

            tasklist_command = f"ps -p {self.pid}"
            tasklist_condition = "/0"
            is_running = self.os.popen(tasklist_command).read()
            if tasklist_condition not in is_running:
                return False
        
        def run_code(self, code):

            self.execute_start = self.time.time()
            self.code = code

            result = self.is_safe(self.code)
            if not result[0]:
                self.exec_time = self.time.time() - self.execute_start
                return [result[1], self.exec_time]
            else:
                self.code = code
                with open(self.execute_filename, "w") as file:
                    file.write(self.code)
                self.worker()

                end = self.time.time() + self.timeout_worker
                while self.time.time() < end:
                    self.time.sleep(self.check_script_timeout)
                    if self.check_if_running() == False:
                        output = self.worker(do_return=True)
                        return output

                self.os.kill(self.pid, self.signal.SIGTERM)
                self.exec_time = self.time.time() - self.execute_start
                return [self.error_timeout, self.exec_time]

        def is_safe(self, code=None):

            if code == None:
                if hasattr(self, "code"):
                    code = self.input_code
                    code_lines = code.split("\n")
            else:
                code_lines = code.split("\n")
            
            for line in code_lines:
                if "import" in line:
                    line = line.replace("import", "").replace(" ", "")
                    modules = line.split(",")
                    for module in modules:
                        if module not in self.trust_modules:
                            return [False, self.error_untrusted_module]

            for keyword in self.dangerous_keywords:
                if keyword in code:
                    error = self.error_dangerous_keyword.replace("$1", keyword)
                    return [False, error]

            return [True, ""]