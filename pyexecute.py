################################################################

import os
import time
import ast
import subprocess
import signal

import const

################################################################

class ExecTimeoutError(Exception):
    pass

class UnsafeCodeError(Exception):
    pass

################################################################

class Result:

    def __init__(self, stdout, stderr, exec_time):

        self.stdout = stdout
        self.stderr = stderr
        self.exec_time = exec_time

################################################################

class PyExecute:

    class _Task:

        def __init__(self, executor, code):

            self.executor = executor
            self.code = code

        def is_running(self):

            if self.executor.win:
                tasklist_cmd = f'tasklist /FI "pid eq {self.pid}"'
                tasklist_cond = "INFO: No tasks are running"
            else:
                tasklist_cmd = f"ps -p {self.pid}"
                tasklist_cond = "<defunct>"
            tasklist = os.popen(tasklist_cmd).read()
            return tasklist_cond not in tasklist

        def run(self):

            self.exec_start = time.time()
            with open(self.executor.file_path, "w", encoding="utf-8") as file:
                file.write(self.code)

            popen_args = [self.executor.python_cmd, self.executor.file_path]
            popen_kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
            if self.executor.win:
                popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
            self.process = subprocess.Popen(popen_args, **popen_kwargs)
            self.pid = self.process.pid

    def __init__(self, filename, timeout=5, checks_per_second=40, python_cmd=None):

        self.filename = filename
        self.timeout = timeout
        self.check_interval = 1 / checks_per_second

        current_dir = os.path.dirname(__file__)
        current_path = os.path.abspath(current_dir)
        self.file_path = os.path.join(current_path, filename)
        self.win = os.name == "nt"
        self.python_cmd = python_cmd or ("python" if self.win else "python3")

    def scan(self, code):

        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in const.banned_names:
                raise UnsafeCodeError(node.id)
            if isinstance(node, ast.Attribute) and node.attr in const.banned_names:
                raise UnsafeCodeError(node.attr)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in const.allowed_modules:
                        raise UnsafeCodeError(alias.name)
            if isinstance(node, ast.ImportFrom) and node.module not in const.allowed_modules:
                raise UnsafeCodeError(node.module)

    def execute(self, code, admin=False):

        code = code.strip(" \t\n")
        task = self._Task(self, code)
        if not admin:
            self.scan(code)
        task.run()

        limit = time.time() + self.timeout
        while time.time() < limit:
            time.sleep(self.check_interval)
            if not task.is_running():
                result = task.process.communicate()
                stdout, stderr = [bytestr.decode("utf-8").strip() for bytestr in result]
                exec_time = time.time() - task.exec_start
                return Result(stdout, stderr, exec_time)

        kill_signal = signal.CTRL_C_EVENT if self.win else signal.SIGTERM
        os.kill(task.pid, kill_signal)
        raise ExecTimeoutError(time.time() - task.exec_start)

################################################################
