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

### 5. AI Criticism Agent (`criticize.py`)
This project includes a sophisticated, AI-powered criticism agent that acts as an automated code reviewer. It analyzes your staged code changes and provides a detailed critique based on project context, coding best practices, and overall quality.

**How it Works:**
The script gathers token-friendly context about your project, including:
- A summary of recent commit subjects.
- A pruned file tree of the repository.
- The `git diff` of your staged changes with extra context lines.
- The project's `README.md` for high-level goals.

This context is then sent to the Gemini API to generate a structured and constructive code review.

## Getting Started

### For the TypeScript Environment
1.  **Install dependencies:**
    ```bash
    npm install
    ```
2.  **Start coding!**
    - For real-time feedback, run `npm run watch:lint` in a separate terminal.
    - When you're ready to commit, use `git add` and `git commit` as usual. Husky will protect your branches from any code that doesn't meet the linting standards.

### For the AI Criticism Agent
1.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up your API Key:**
    The agent requires a Gemini API key to function. Set it as an environment variable.
    ```bash
    # For Windows
    set GEMINI_API_KEY="YOUR_API_KEY"

    # For macOS/Linux
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```
    You can obtain a key from [Google AI Studio](https://aistudio.google.com/).

3.  **Run the Agent:**
    After you have staged some changes with `git add`, you can run the agent to get a review.
    ```bash
    python criticize.py
    ```

