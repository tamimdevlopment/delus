# Delus

A set of super lightweight, zero-dependency code generators and compilers written in pure Python. It provides automated context managers (`with` scopes) to generate clean, highly-optimized C and Assembly code without the overhead of heavy Abstract Syntax Trees (AST).

## Why this exists?
Traditional decompilers and transpilers rely on massive AST parsing trees and external dependencies (like LLVM). This project implements an elegant, pure Python Builder Pattern that tracks register allocations and memory states directly via Python's `__enter__` and `__exit__` magic methods. It generates fast, naked, and obfuscated-ready outputs.

## License
This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. You are free to use, modify, and redistribute this software, provided that any derivative work remains open-source under the same license terms, ensuring explicit patent protections for all contributors and users.

## Contribution & Development
This is a hacker-centric project. We welcome and encourage anyone to contribute to this repository. You are completely free to submit a Pull Request with a brand new code architecture, or suggest refactoring and optimizations for the existing codebase.

Feel free to clone the repository, write your modules, and help us make compilers simpler.
