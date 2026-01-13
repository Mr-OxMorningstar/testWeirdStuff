# TypeScript Project with an Integrated "Criticism Agent"

This project is configured with a robust development environment designed to enforce high code quality and provide immediate feedback. It uses a combination of ESLint for static analysis and Husky for Git hooks to act as an automated "criticism agent."

## Features

### 1. Code Quality with ESLint
The project uses **ESLint** along with plugins for **TypeScript** (`@typescript-eslint/eslint-plugin`). This helps in identifying and fixing problems in your TypeScript code. The configuration is defined in `.eslintrc.json` and extends the recommended rules for both ESLint and TypeScript.

### 2. Manual Linting
You can manually run the linter across the entire project at any time. This is useful for checking the whole codebase at once.

**Command:**
```bash
npm run lint
```

### 3. Real-time Linting (Automated Criticism)
For instant feedback while you code, you can start a file watcher. This process monitors all TypeScript files (`.ts`, `.tsx`) for changes and automatically runs the linter on them when you save. This is the "awesome" real-time errors feature.

**Command:**
```bash
npm run watch:lint
```
It's recommended to keep this command running in a separate terminal window while you work.

### 4. Pre-commit Gatekeeper
To ensure that no code with linting errors is committed to the version history, **Husky** has been configured to run a `pre-commit` hook. Before any `git commit` is finalized, this hook will automatically execute `npm run lint`. If any errors are found, the commit will be aborted, forcing you to fix the issues before proceeding. This acts as a final quality gate.

## Getting Started

1.  **Install dependencies:**
    ```bash
    npm install
    ```
2.  **Start coding!**
    - For real-time feedback, run `npm run watch:lint` in a separate terminal.
    - Write your TypeScript code.
    - When you're ready to commit, use `git add` and `git commit` as usual. Husky will protect your branches from any code that doesn't meet the linting standards.
