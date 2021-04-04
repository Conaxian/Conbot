import conscript

class ConExecute:

    def __init__(self, client, ctx):

        self.client = client
        self.ctx = ctx
    
    async def execute(self, code):

        output, error = conscript.run("conexecute.py", code)

        return str(error) if error else output