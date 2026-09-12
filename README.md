# Delus

A set of super lightweight, zero-dependency code generators and compilers written in pure Python. It provides automated context managers (`with` scopes) to generate clean, highly-optimized C and Assembly code without the overhead of heavy Abstract Syntax Trees (AST).

## Why this exists?
Traditional decompilers and transpilers rely on massive AST parsing trees and external dependencies (like LLVM). This project implements an elegant, pure Python Builder Pattern that tracks register allocations and memory states directly via Python's `__enter__` and `__exit__` magic methods. It generates fast, naked, and obfuscated-ready outputs.

## License
This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. You are free to use, modify, and redistribute this software, provided that any derivative work remains open-source under the same license terms, ensuring explicit patent protections for all contributors and users.

## Contribution & Development
This is a hacker-centric project. We welcome and encourage anyone to contribute to this repository. You are completely free to submit a Pull Request with a brand new code architecture, or suggest refactoring and optimizations for the existing codebase.

Feel free to clone the repository, write your modules, and help us make compilers simpler.

## Quick Examples

### 1. C Generation Example
```python
if __name__ == "__main__":
    program = Mylang()
    program.add_lib("cstdio")

    with program.function(program, "main", "int") as main:
        with main.for_loop("int i = 0", "i<10", "i++"):
            with main.if_condintion("i % 2 == 0"):
                main.print("i", variable=True)
        main.return_val("0")
        
    print(program.run())
```

### 2. Assembly Generation Example
```python
if __name__ == "__main__":
    mylan = mylang()
    mylan.create_func("counter")
    mylan.create_func("out")
    mylan.create_func("check")
    
    mylan.sys_exit(0, "out")
    mylan.print("hello world", "counter")
    mylan.newline("counter")
    mylan.decrease("r10", "counter")
    mylan.mov("r10", "10", "_start")
    mylan.jmp("check", "_start")
    mylan.cmp("r10", "0", jmp_if_equal="out", jmp_if_not_equal="counter", func="check")
    mylan.jmp("check", "counter")
    
    print(mylan.run())
```
