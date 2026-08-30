# Agent development guide

This repository is primarily coursework and learning material. Preserve the educational intent: prefer clear, idiomatic Python and explanations over unnecessary abstractions.

## Workflow

1. Read `PLAN.md`, the root `README.md`, and the README for the specific module/week before changing exercises.
2. Verify Python/library behavior against current official documentation when needed; Context7 may assist with current docs.
3. Keep solutions understandable at the level of the course. Do not introduce frameworks, complex patterns, or dependencies unless the exercise explicitly needs them.
4. Preserve expected inputs/outputs and assignment requirements.
5. Add focused tests for reusable or non-trivial logic where practical; run existing CI and the tests for the touched week.
6. Treat example files and user input defensively, but do not overengineer classroom scripts.
7. Document meaningful refactors or tooling changes in `PLAN.md`.

## Review roles

For larger coursework projects, perform separate implementation and test/readability reviews. Security review is appropriate when an exercise handles files, network input, credentials, or external APIs.

## Completion gate

A change is complete when the relevant exercise still matches the assignment, tests/CI pass, and the code remains easy for a learner to explain line by line.
