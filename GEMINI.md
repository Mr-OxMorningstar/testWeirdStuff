
# GEMINI.md - Project Analysis

## Project Overview

This project is a Python-based toolkit for interacting with Google's Generative AI models, primarily focusing on the **Gemini** and **Gemma** families. It appears to provide a comprehensive set of tools for various use cases, from simple API calls to complex model processing and evaluation.

The core purpose is to provide a robust interface for leveraging these models, with functionalities including:

*   **Multi-backend Gemini Integration:** The system can interact with Gemini models through various backends, including the standard Google AI (Gemini API), Vertex AI, and third-party services like OpenRouter.
*   **Asynchronous and Parallel Processing:** The codebase includes sophisticated, production-ready features like asynchronous API calls (`async/await`), streaming responses, and parallel request execution using thread pools.
*   **Model Conversion:** The project includes tools for converting Gemma models into the `gguf` format, which is optimized for local inference with engines like `llama.cpp`.
*   **Schema Transformation for Tooling:** There is a significant focus on function calling (tool use), with dedicated logic for converting OpenAPI schemas into the format required by the Gemini API.
*   **Benchmarking and Evaluation:** The project contains scripts and configurations for running performance benchmarks against Gemini models.

**Key Technologies:**
*   **Language:** Python
*   **Models:** Gemini (1.5-flash, 2.0-flash), Gemma, Gemma2
*   **APIs:** Google Generative AI, Google Vertex AI, OpenRouter
*   **Frameworks/Libraries:** `pytest` (for testing), `gguf` (for model quantization), `ThreadPoolExecutor` (for concurrency).

## Building and Running

The project is structured as a Python application/library. While explicit dependency files (`requirements.txt`) were not provided, the following commands can be inferred.

### Dependencies

It's highly likely the project uses a `requirements.txt` file. To install dependencies, run:
```bash
pip install -r requirements.txt
```
Key dependencies would include `google-generativeai`, `google-cloud-aiplatform`, `pytest`, and potentially libraries for handling `gguf` files.

### Running Tests

The project uses `pytest` for its test suite. The `TestToGeminiSchema` class demonstrates a clear testing structure. To run the full test suite:
```bash
pytest
```

## Development Conventions

*   **Typing:** The code consistently uses Python's type hints (e.g., `model_name: str`, `prompts: List[str]`), indicating a convention of strong typing to improve code quality and maintainability.
*   **Testing:** Tests are written using the `pytest` framework. Test classes (e.g., `TestToGeminiSchema`) and methods (`test_*`) are the standard. The tests are comprehensive, covering various edge cases for the schema conversion logic.
*   **Asynchronous Code:** The `Gemini` class heavily utilizes `async/await` for non-blocking I/O, which is a best practice for applications involving network requests to external APIs.
*   **Linting:** The presence of `pylint: disable=...` comments suggests that `pylint` is used to enforce code style and catch errors, with developers consciously overriding it where necessary.
*   **Modularity:** The code is organized into classes with specific responsibilities (`GeminiModel`, `GemmaModel`, `Gemini` class inheriting from a `BaseLlm`), which points to a modular and extensible architecture.
*   **Configuration:** Configuration is handled via dedicated functions (e.g., `setup_gemini_config`) and passed as dictionaries or objects, promoting a clean separation of configuration from logic.

## Development Environment Setup (TypeScript Criticism Agent)

To ensure high code quality and provide immediate feedback for TypeScript development, a "criticism agent" has been integrated into the project. This agent leverages ESLint, `chokidar-cli`, and Husky.

### ESLint for TypeScript
*   **Purpose:** Static analysis for TypeScript code. It checks for style, errors, and best practices.
*   **Configuration:** Located in `.eslintrc.json`, extending recommended rules from `eslint:recommended` and `plugin:@typescript-eslint/recommended`.
*   **Manual Run:** `npm run lint`

### Real-time Linting
*   **Tool:** `chokidar-cli`
*   **Purpose:** Monitors TypeScript files for changes and automatically runs `npm run lint` upon saving. Provides instant feedback.
*   **Command:** `npm run watch:lint` (run in a separate terminal)

### Git Pre-commit Hook
*   **Tool:** Husky
*   **Purpose:** Blocks `git commit` operations if staged TypeScript files contain linting errors. Ensures only quality code enters the version history.
*   **Mechanism:** A `pre-commit` hook (configured via Husky) executes `npm run lint` on staged changes before allowing a commit.

