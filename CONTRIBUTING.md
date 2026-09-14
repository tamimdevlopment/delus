# Contributing to Delus

Welcome to Delus. This project is a hacker-centric, lightweight, zero-dependency multi-language transpiler stack written in pure Python. The goal is to generate clean, highly-optimized code for various target languages using Python's context managers without the overhead of massive abstract syntax trees (AST).

We aim to grow this project into a sustainable, community-driven ecosystem. The contribution workflow is inspired by the Linux Kernel development model, focusing on progressive trust and technical merit rather than academic bureaucracy. Think of it as a practical diploma in compiler engineering rather than a corporate Ph.D. defense.

---

## The Trust Hierarchy

To maintain code quality and security, we use a merit-based progression system. Your access and influence in the repository scale with your track record of accepted patches:

1. Contributor: Anyone can submit a Pull Request (PR). If your code passes review, fixes an issue, or introduces a clean compiler target module without regression, it gets merged.
2. Trusted Developer: After multiple successful PRs, you gain code ownership over specific language targets. Your reviews carry weight for new incoming patches.
3. Sub-Maintainer: High-trust contributors who consistently deliver optimized code will be responsible for managing subsystems, reviewing external code, and filtering PRs.
4. Core Merge: Tamim (tamimdevlopment) handles the final quality assurance and merges approved subsystem branches into the master repository.

---

## Code Architecture & Target Rules

Every submitted patch must strictly adhere to the project's minimalist philosophy:

* Zero External Dependencies: No heavy parsing libraries, no LLVM wrappers. Use pure, standard Python.
* Maintain the Builder Pattern: Leverage Python's __enter__ and __exit__ magic methods inside the code generators to ensure clean, structured scopes across all target languages.
* Expand Target Languages: Choose any target programming or scripting language you are interested in, write its transpiler module using our syntax, and submit a PR to add it to the project.
* Raw Output Optimization: The generated target code must be raw, fully naked, and optimal for execution or obfuscation passes.
* Readability: While generated code may look obfuscated, the generator logic inside Delus must be highly readable and maintainable.

---

## Submission Workflow

1. Fork the repository and create your feature branch.
2. Check the open issues or implement a brand new target language module of your choice.
3. Verify that your builder output produces valid, compile-ready files for the specific target language.
4. Open a clean Pull Request explaining the architectural changes or optimizations you made. Your patch will be reviewed, and your trust score in the project will be updated accordingly.
