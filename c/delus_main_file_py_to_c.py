class Mylang:
    def __init__(self):
        self.funcs = {}
        self.code = []
    def add_lib(self,lib):
        self.code.append("#include <{}>\n".format(lib))
    class function:
        def __init__(self,parent,name:str,return_type:str,args:str=""):
            self.parent = parent
            self.code = []
            self.name = name
            self.return_type = return_type
            self.args = args
        def print(self,text,variable=False,type="%d"):
            self.code.append("\tprintf({});\n".format(f'"{text}"' if not variable else f'"{type}",' + text))
        def assign_variable(self,variablename:str,value,new=False,type="None"):
            self.code.append("\t{}{} = {};\n".format(type + " " if new else "",variablename,value))
        def __enter__(self):
            self.code.append("{} {}({}) {{\n".format(self.return_type, self.name,self.args))
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.code.append("}\n\n")
            self.parent.code.extend(self.code)
        class _IF:
            def __enter__(self):
                self.start_index = len(self.func.code)
                return self
            def __exit__(self, exc_type, exc, tb):
                inner_code = self.func.code[self.start_index:]
                del self.func.code[self.start_index:]

                formatted = ["\tif ({}\n".format(self.condintion + ") {")]
                for line in inner_code:
                    formatted.append("\t" + line)
                formatted.append("\t}\n")
                self.func.code.extend(formatted)
        class _WHILE:
            def __enter__(self):
                self.start_index = len(self.func.code)
                return self
            def __exit__(self, exc_type, exc, tb):
                inner_code = self.func.code[self.start_index:]
                del self.func.code[self.start_index:]
        
                formatted = ["\twhile ({}\n".format(self.condintion + ") {")]
                for line in inner_code:
                    formatted.append("\t" + line)
                formatted.append("\t}\n")
                self.func.code.extend(formatted)
        class _FOR:
            def __enter__(self):
                self.start_index = len(self.func.code)
                return self
            def __exit__(self, exc_type, exc, tb):
                inner_code = self.func.code[self.start_index:]
                del self.func.code[self.start_index:]
        
                formatted = ["\tfor ({}) {{\n".format(";".join([self.variable, self.condintion, self.update]))]
                for line in inner_code:
                    formatted.append("\t" + line)
                formatted.append("\t}\n")
                self.func.code.extend(formatted)
        def for_loop(self,variable_assignment:str,condintion:str,update:str):
            scope = self._FOR()
            scope.func = self
            scope.condintion = condintion
            scope.variable = variable_assignment
            scope.update = update
            return scope
        def while_loop(self,condintion:str):
            scope = self._WHILE()
            scope.func = self
            scope.condintion = condintion
            return scope
        def if_condintion(self,condintion:str):
            scope = self._IF()
            scope.func = self
            scope.condintion = condintion
            return scope
        def call(self,function:str,args:str = "()"):
            self.code.append("\t{}{};\n".format(function,args))
        def return_val(self,return_value:str):
            self.code.append("\treturn {};\n".format(return_value))
    def run(self):
        return "".join(self.code)
    
if __name__ == "__main__":
    program = Mylang()
    program.add_lib("cstdio")

    with program.function(program,"main","int") as main:
        with main.for_loop("int i = 0","i<10","i++"):
            with main.if_condintion("i % 2 == 0"):
                main.print("i",variable=True)
        main.return_val("0")
            

    print(program.run())
