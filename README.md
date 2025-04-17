# Sequence Alignment: Dynamic Programming and Memory-Efficient Solutions

This repository contains two Python implementations of the **Sequence Alignment** problem using:
- A classic **Dynamic Programming** approach
- A **Memory-Efficient Divide-and-Conquer** optimization

The goal is to align two DNA sequences (`A`, `C`, `G`, `T`) with the lowest possible mismatch and gap cost. This project explores the performance trade-offs between full-memory DP solutions and space-optimized algorithms.

## 🔍 Problem Overview

Given two nucleotide sequences, the objective is to compute the **minimum-cost alignment** between them based on:
- A **gap penalty** for unmatched characters
- A **mismatch matrix** defining the cost of aligning different nucleotides

This type of alignment is widely used in computational biology for genome comparison and similarity analysis.

## 💡 Key Features

- Implements both **standard DP** and **Hirschberg’s memory-optimized** techniques
- Supports **automated input parsing** and recursive string generation
- Measures and reports **execution time** and **peak memory usage**
- Outputs alignment results and statistics to a file in a structured format

## 🧪 Input Format

Input files are structured to define a base string and a series of numeric transformation steps that recursively build larger DNA strings. Example:

Each integer indicates an insertion index. Each step doubles the string length by embedding the current string into itself.

## 🧾 Output Format

Each alignment execution produces an output file containing:
1. Minimum alignment cost (integer)
2. First aligned string (includes gaps `_`)
3. Second aligned string (includes gaps `_`)
4. Runtime (milliseconds)
5. Memory used (KB)

## 🛠️ How to Run

Make sure you have Python 3 and `psutil` installed:

```bash
pip install psutil
