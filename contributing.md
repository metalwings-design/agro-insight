# Contributing to Agro-Insight
Thank you for your interest in contributing to our open-source project! We welcome all contributions, including bug reports, documentation updates, feature requests, and code contributions.

## How to Contribute
## 1. Reporting Bugs & Feature Requests
Check the existing Issues tab to ensure it has not already been reported.

Open a new issue with a clear title and description.

Provide specific steps to reproduce the bug, along with error logs and system environment details if applicable.

## 2. Code Contributions
Fork the Repository: Create a personal copy of the repository on GitHub.

Clone Locally: Clone your fork to your machine and set up the local directory structure as detailed in replicate.md.

Implement Configurations: Ensure all file paths use the established relative path structure (BASE_PATH). Do not hardcode local directories.

Test Changes: Run the processing script (code3_replicate.py) and launch the Streamlit dashboard locally to verify functionality.

Commit and Push: Write clear, concise commit messages. Push changes to your fork.

Submit a Pull Request (PR): Open a PR against the main repository. Provide a detailed summary of the changes made and link any related issues.

## Formatting & Code Style
Data Formats: Keep tabular datasets isolated in .csv format rather than multi-sheet .xlsx files to maintain clean version control diffs.

Documentation: Write and update all guides strictly in Markdown (.md) format.

Code Clarity: Group parameters and file paths inside the global configuration section at the top of the script files.

## Community Standards
By contributing to this project, you agree to abide by our Code of Conduct in all interactions. Maintainers reserve the right to reject contributions that do not align with these standards.