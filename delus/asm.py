import uuid

class mylang:
    def __init__(self):
        self.bss = ["section .bss\n"]
        self.text = ["section .text\n global _start\n\n"]
        self.data = ["section .data\n"]
        self.funcs = {"_start":[]}
        self.cache = {}
        self.code = []
        self.regs = {}
        self.called = set(["_start"])
    def precheck(self):
                if self.regs.get("rax") is None:
                    self.regs.setdefault("rax",999)
                if self.regs.get("rdi") is None:
                    self.regs.setdefault("rdi",999)
                if self.regs.get("rdx") is None:
                    self.regs.setdefault("rdx",999)
                if self.regs.get("rsi") is None:
                    self.regs.setdefault("rsi",999)
                if self.regs.get("al") is None:
                    self.regs.setdefault("al",999)
    def safecheck_print(self,text,uui) -> list:
        cmd = ["\tmov rax,1\n"]
        self.regs["rax"] = 1
        if self.regs["rdi"] != 1:
            cmd.append("\tmov rdi,1\n")
            self.regs["rdi"] = 1
        if self.regs["rdx"] != len(text):
            cmd.append("\tmov rdx,str_{}len\n".format(uui))
            self.regs["rdx"] = len(text)
        if self.regs["rsi"] != text:
            cmd.append("\tmov rsi,str_{}\n".format(uui))
            self.regs["rsi"] = text
        return cmd
    def safecheck_input(self,buf:str,size:int):
        cmd = ["\tmov rax,0\n"]
        self.regs["rax"] = 0
        if self.regs["rdi"] != 0:
            cmd.append("\tmov rdi,0\n")
            self.regs["rdi"] = 0
        if self.regs["rdx"] != size:
            cmd.append("\tmov rdx,{}\n".format(size))
            self.regs["rdx"] = size
        if self.regs["rsi"] != buf:
            cmd.append("\tmov rsi,str_{}\n".format(buf))
            self.regs["rsi"] = buf
        return cmd
    def cache_manager(self,text:str):
        if self.cache.get(text) is None:
            uui = str(uuid.uuid4()).replace("-","_")
            self.cache.setdefault(text,uui)
            self.data.append("\tstr_{} db {},0\n".format(uui,'"' + text + '"'))
            self.data.append("\tstr_{}len equ $ - str_{}\n".format(uui,uui))
        else:  
            uui = self.cache.get(text)
        return uui
    def print(self,text:str,func:str):
        uui = self.cache_manager(text)
        self.precheck()
        cmd = self.safecheck_print(text,uui)
        cmd.append("\tsyscall\n")
        self.funcs[func].extend(cmd)
    def sys_exit(self,exitcode:int,func:str,Error:str = None):
        cmd = []
        if Error is not None:
            uui = self.cache_manager(Error)
            cmd = [
                "\tmov rax,1\n",
                "\tmov rdi,2\n",
                "\tmov rdx,str_{}len\n".format(uui),
                "\tmov rsi,str_{}\n".format(uui),
            ]
        cmd.extend([
                "\tmov rax,60\n",
                "\tmov rdi,{}\n".format(exitcode),
                "\tsyscall\n"
            ])
        self.funcs[func].extend(cmd)
    def call(self,func_name:str,func:str):
        self.called.add(func_name)
        self.funcs[func].append("\tcall {}\n".format(func_name))
    def jmp(self,func_name:str,func:str):
        self.called.add(func_name)
        self.funcs[func].append("\tjmp {}\n".format(func_name))
    def mov(self,val1:str,val2:str,func:str):
        self.regs[val1] = val2
        self.funcs[func].append("\tmov {},{}\n".format(val1,val2))
    def cmp(self,val1:str,val2:str,func:str,jmp_if_equal:str = None,jmp_if_not_equal:str = None,jmp_if_greater_than:str = None,jmp_if_greater_or_equal:str = None,jmp_if_less_or_equal:str = None,jmp_if_less:str = None):
        cmd = [
            "\tcmp {},{}\n".format(val1,val2),
        ]
        copy_cmd = [
            "\tcmp {},{}\n".format(val1,val2),
        ]
        if jmp_if_equal is not None:
            cmd.append("\tje {}\n".format(jmp_if_equal))
        if jmp_if_not_equal is not None:
            cmd.append("\tjne {}\n".format(jmp_if_not_equal))
        if jmp_if_greater_than is not None:
            cmd.append("\tjg {}\n".format(jmp_if_greater_than))
        if jmp_if_greater_or_equal is not None:
            cmd.append("\tjge {}\n".format(jmp_if_greater_or_equal))
        if jmp_if_less is not None:
            cmd.append("\tjl {}\n".format(jmp_if_less))
        if jmp_if_less_or_equal is not None:
            cmd.append("\tjle {}\n".format(jmp_if_less_or_equal))
        if copy_cmd == cmd:
            return 0
        self.funcs[func].extend(cmd)
    def lea(self,reg:str,equation:str,func:str):
        self.funcs[func].append("\tlea {},{}\n".format(reg,equation))
    def input(self,func:str,size:int):
        self.precheck()
        uui = str(uuid.uuid4()).replace("-","_")
        self.bss.append("\tstr_{} resb {}\n".format(uui,size))
        cmd = self.safecheck_input(uui,size)
        cmd.append("\tsyscall\n")
        self.funcs[func].extend(cmd)
        return (uui,size)
    def print_buf(self,func:str,buf:tuple[str,int]):
        self.precheck()
        size = buf[1]
        cmd = []
        if self.regs["rdx"] == buf[1]:
            cmd.append("\tmov rdx,rax\n")
            self.regs["rdx"] = 999
            size = -1
        cmd.extend(["\tmov rax,1\n"])
        self.regs["rax"] = 1
        if self.regs["rdi"] != 1:
            cmd.append("\tmov rdi,1\n")
            self.regs["rdi"] = 1
        if self.regs["rdx"] != buf[1] and size == buf[1]:
            cmd.append("\tmov rdx,{}\n".format(buf[1]))
            self.regs["rdx"] = buf[1]
        if self.regs["rsi"] != buf[0]:
            cmd.append("\tmov rsi,str_{}\n".format(buf[0]))
            self.regs["rsi"] = buf[0]
        cmd.append("\tsyscall\n")
        self.funcs[func].extend(cmd)
    def sub(self,val1:str,val2:str,func:str):
        self.funcs[func].extend([
            "\tsub {},{}\n".format(val1,val2)
        ])
        self.regs[val1] = 999
    def multiply(self,val1:str,val2:str,func:str):
        self.funcs[func].extend([
            "\timul {},{}\n".format(val1,val2)
        ])
        self.regs[val1] = 999
        self.regs["rax"] = 999
    def increase(self,val:str,func:str):
        self.funcs[func].extend([
                    "\tinc {}\n".format(val)
                ])
        self.regs[val] = 999
    def decrease(self,val:str,func:str):
        self.funcs[func].extend([
                    "\tdec {}\n".format(val)
                ])
        self.regs[val] = 999
    def subtract(self,val1:str,val2:str,func:str):
        self.funcs[func].extend([
            "\tsub {},{}\n".format(val1,val2)
        ])
        self.regs[val1] = 999
    def newline(self,func:str):
        self.precheck()
        cmd = [
            "\tpush 10\n",
            "\tmov rax, 1\n",
            "\tmov rdi, 1\n",
            "\tmov rsi, rsp\n",
            "\tmov rdx, 1\n",
            "\tsyscall\n",
            "\tpop rcx\n"
        ]
        self.regs["rax"] = 999 
        self.regs["rdx"] = 1
        self.regs["rsi"] = 999
        
        self.funcs[func].extend(cmd)
    def run(self):
        self.code.extend(self.bss)
        self.code.extend(self.data)
        self.code.extend(self.text)
        for k,v in self.funcs.items():
            if not v:
                continue
            self.code.append("{}:\n".format(k))
            self.code.extend(v)
        return "".join(self.code)
    def create_func(self,func_name:str):
        self.funcs.setdefault(func_name,[])


if __name__ == "__main__":
    mylan = mylang()
    mylan.create_func("counter")
    mylan.create_func("out")
    mylan.create_func("check")
    mylan.sys_exit(0,"out")
    mylan.print("hello world","counter")
    mylan.newline("counter")
    mylan.decrease("r10","counter")
    mylan.mov("r10","10","_start")
    mylan.jmp("check","_start")
    mylan.cmp("r10","0",jmp_if_equal="out",jmp_if_not_equal="counter",func="check")
    mylan.jmp("check","counter")
    print(mylan.run())
