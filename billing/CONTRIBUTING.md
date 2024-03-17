# Contribution Guidelines

Thank you for considering contributing to our project! We appreciate your interest and support. Before getting started, please review the following guidelines to ensure smooth collaboration and maintain high-quality standards.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Forking the Repository](#forking-the-repository)
   - [Setting Up Your Development Environment](#setting-up-your-development-environment)
3. [Contributing Code](#contributing-code)
   - [Naming Conventions](#naming-conventions)
   - [Coding Standards](#coding-standards)
   - [Writing Tests](#writing-tests)
   - [Logging](#logging)
4. [Submitting Changes](#submitting-changes)
   - [Commit Message Guidelines](#commit-message-guidelines)
   - [Pull Request Process](#pull-request-process)
5. [Review Process](#review-process)
6. [Additional Resources](#additional-resources)

## Introduction

This document outlines the guidelines for contributing to our project. Whether you're fixing a bug, adding a feature, or improving documentation, your contributions are valued and encouraged.

## Getting Started

### How to Execute server

TODO

### Setting Up Your Development Environment

TODO

## Contributing Code

### Naming Conventions

When naming variables, functions, classes, and files, adhere to the following conventions:
- Use meaningful and descriptive names.
- Avoid abbreviations and acronyms unless widely recognized.
- for functions/methods: decide
- for variables: decide
<!-- - Follow consistent casing (camelCase, snake_case, etc.). -->

### Coding Standards

Maintain consistent coding style throughout the project:
TODO: decide
<!-- - Follow the established coding style guide (e.g., PEP 8 for Python). -->
- Use clear and concise comments to explain complex logic.
- Ensure proper indentation and formatting.

### Writing Tests

All new features and bug fixes must include corresponding tests:
- Write unit tests to cover the functionality of your code.
- Ensure existing tests pass before submitting changes.
- Aim for high test coverage to minimize regressions.

### Logging

Include appropriate logging statements to facilitate troubleshooting and debugging:
- TODO: Show usage
- Log relevant information, warnings, and errors.
- Use descriptive log messages to provide context.

## Submitting Changes

### Commit Message Guidelines

Follow best practices for writing commit messages:
- Use imperative mood in the subject line (e.g., "Fix typo" instead of "Fixed typo").
- Keep subject lines concise and descriptive.
- Include a detailed commit body if necessary.

### Push and merge Guidelines
- Before starting to change the code, pull the grand-truth branch,
- From there checkout to your own branch.
- Make the changes
- Check that they are working properly (if it is a route, use postman and check that you get the desired values in the response. Until we use unit testing)
- Then add and commit the changes to your remote branch.
- Do a back merge with the branch that is the grand truth.
- Handle conflicts and check that you didn't destroy anything in the grand truth branch.
- If everything works as it should:
Make a pull request and ask to merge your current branch with the grand truth branch.


### Pull Request Process

When submitting changes, follow these steps:

TODO: decide

0. make sure your branch is ff-merge with the origin/<branch-name>
1. Create a new branch for your feature or fix.
2. Commit your changes with clear messages.
3. Push your branch to your forked repository.
4. Open a pull request against the main project repository.

## Review Process

All pull requests will undergo code review to ensure quality and adherence to guidelines. Be open to feedback and address any requested changes promptly.

## Additional Resources

For further information and assistance, refer to the following resources:
- Project documentation
- Community forums
- Contact information for maintainers
