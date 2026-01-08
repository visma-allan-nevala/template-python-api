# Working Documents

This folder is for local working documents that should **not** be committed to Git.

## Purpose

Use this folder for:
- Analysis notes and scratch work
- Local reference materials
- Draft documentation
- Personal notes during development
- Downloaded reference files (PDFs, CSVs, etc.)

## Gitignore

All files in this folder (except this README and .gitkeep) are gitignored.

This allows developers to keep project-related files organized locally without cluttering the repository.

## Examples

```
working_docs/
├── .gitkeep
├── README.md           (committed)
├── analysis-notes.md   (ignored)
├── api-research.md     (ignored)
├── meeting-notes/      (ignored)
└── reference/          (ignored)
    ├── spec.pdf
    └── data-sample.csv
```
