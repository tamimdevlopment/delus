class Mojo:
    def __init__(self):
        self.code = []
    class fn:
        def __init__(self,parent,function_name:str,return_Value:str,args:str="",):
            self.parent = parent
            self.function_name = function_name
            self.args = args
            self._return_value = return_Value
        def __enter__(self):
            self.start_index = len(self.parent.code)
            return self
        def __exit__(self, exc_type, exc, tb):
            code = self.parent.code[self.start_index:]
            del self.parent.code[self.start_index:]
            formatted = ["fn {}({}) -> {}:\n".format(self.function_name,self.args,self._return_value)]
            for i in code:
                formatted.append("\t" + i)
            formatted.append("\n")
            self.parent.code.extend(formatted)
        class _IF:
            def __enter__(self):
                self.start_index = len(self.parent.code)
            def __exit__(self, exc_type, exc, tb):
                code = self.parent.code[self.start_index:]
                del self.parent.code[self.start_index:]
                formatted = ["{}:\n".format(self.command_if_else_elif)]
                for i in code:
                    formatted.append("\t" + i)
                formatted.append("\n")
                self.parent.code.extend(formatted)
        class _WHILE:
            def __enter__(self):
                self.start_index = len(self.parent.code)
            def __exit__(self, exc_type, exc, tb):
                    code = self.parent.code[self.start_index:]
                    del self.parent.code[self.start_index:]
                    formatted = ["while {}:\n".format(self.condition)]
                    for i in code:
                        formatted.append("\t" + i)
                    formatted.append("\n")
                    self.parent.code.extend(formatted)
        class _FOR:
            def __enter__(self):
                self.start_index = len(self.parent.code)
            def __exit__(self, exc_type, exc, tb):
                code = self.parent.code[self.start_index:]
                del self.parent.code[self.start_index:]
                formatted = ["for {} in {}:\n".format(self.variable_name,self.iterate)]
                for i in code:
                    formatted.append("\t" + i)
                formatted.append("\n")
                self.parent.code.extend(formatted)
        def for_loop(self,variable_name:str,the_iterator:str):
            scope = self._FOR()
            scope.variable_name = variable_name
            scope.iterate = the_iterator
            scope.parent = self.parent
            return scope
        def while_loop(self,condition:str):
            scope = self._WHILE()
            scope.condition = condition
            self.parent = self.parent
            return scope
        def if_condition(self,condition:str):
            scope = self._IF()
            scope.command_if_else_elif = "if {}".format(condition)
            scope.parent = self.parent
            return scope
        def else_condition(self):
            scope = self._IF()
            scope.command_if_else_elif = "else"
            scope.parent = self.parent
            return scope
        def elif_condition(self,condition:str):
            scope = self._IF()
            scope.command_if_else_elif = "elif {}".format(condition)
            scope.parent = self.parent
            return scope
        def print(self,text:str):
            self.parent.code.append("print({})\n".format(text))
        def return_value(self,value):
            self.parent.code.append("return {}".format(value))
        def assign_variable(self, variable_name: str, value, var_type: str = ""):
            if var_type == "":
                self.parent.code.append("var {} = {}\n".format(variable_name, value))
            else:
                self.parent.code.append("var {}: {} = {}\n".format(variable_name, var_type, value))
        def call(self,function_name:str,args:str=""):
            self.parent.code.append("{}({})\n".format(function_name,args))
        def comment(self,text:str):
            self.parent.code.append("# {}\n".format(text))
    def run(self):
        return "".join(self.code)
        

if __name__ == "__main__":
    program = Mojo()

    with program.fn(program,"main","int") as main:
        with main.for_loop("i","range(2,10)"):
            with main.if_condition("i % 2 == 0"):
                main.print('"even : ",i')
        main.return_value(0)
    print(program.run())
