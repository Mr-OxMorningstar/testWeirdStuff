
import subprocess
import sys
import os
import re
import google.genai as genai

# --- Configuration ---
# Fetch the API key from environment variables
client = genai.Client()

# --- Context Gathering Functions ---

def run_command(command):
    """A helper function to run shell commands and return the output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            return f"Error running command '{' '.join(command)}':\n{result.stderr}"
        return result.stdout
    except FileNotFoundError:
        return f"Error: Command '{command[0]}' not found. Is it installed and in your PATH?"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_staged_diff_with_context():
    """
    Retrieves the staged changes from Git with a larger context window for better analysis.
    -U10 provides 10 lines of context around each change.
    """
    return run_command(['git', 'diff', '--staged', '-U10'])

def get_git_log_subjects():
    """
    Retrieves the subjects of the last 15 commits to understand recent project velocity.
    """
    return run_command(['git', 'log', '-n', '15', '--pretty=format:"%s"'])

def get_file_tree():
    """
    Generates a pruned file tree of the repository, ignoring common noise.
    """
    ignore_dirs = ['.git', 'node_modules', '__pycache__', 'dist', 'build']
    path_list = []
    for root, dirs, files in os.walk("."):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for name in files:
            path_list.append(os.path.join(root, name))
    
    return "\n".join(path_list)

def get_file_content(file_path):
    """Reads the content of a specified file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except FileNotFoundError:
        return f"Warning: File not found: {file_path}"
    except Exception as e:
        return f"Warning: Could not read file {file_path}: {e}"

# --- AI Interaction ---

def get_ai_criticism(prompt: str):
    """
    Sends the provided prompt to the Gemini API and returns the criticism.
    """
    try:
        print("Generating AI criticism... (this may take a moment)")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the Gemini API: {e}"

# --- Main Orchestrator ---

def main():
    """
    Main function for the AI-powered criticize agent.
    """
    print("--- Running AI Criticism Agent (Phase 1) ---")

    # 1. Gather all context
    print("Gathering project context...")
    readme_content = get_file_content("README.md") or get_file_content("GEMINI.md") or "No overview document found."
    git_log_content = get_git_log_subjects()
    file_tree_content = get_file_tree()
    staged_diff_content = get_staged_diff_with_context()

    if "not a git repository" in staged_diff_content:
        print("Error: This script must be run within a Git repository.", file=sys.stderr)
        sys.exit(1)

    if not staged_diff_content.strip() or "Error" in staged_diff_content:
        print("No staged changes found or error retrieving diff. Add files with 'git add' before running.")
        return

    # 2. Construct the Master Prompt
    system_prompt = f"""
You are a world-class senior software engineer and code reviewer. Your task is to provide a thorough, constructive, and actionable critique of the code changes provided below. Your analysis must be based on the complete context provided: the project's purpose, its recent history, its file structure, and the specific changes being introduced.

**CRITICAL INSTRUCTIONS:**
1.  **Analyze Holistically:** Do not just look at the changed lines. Evaluate how they fit into the overall project.
2.  **Adhere to Conventions:** Check if the changes align with the style and patterns from the project's recent commit history.
3.  **Identify Risks:** Look for potential bugs, security vulnerabilities, and anti-patterns.
4.  **Be Constructive:** Your goal is to help the developer improve the code. Frame your feedback positively.
5.  **Output Format:** Provide your response in Markdown with the specified structure: "Overall Assessment", "Code Quality Score", "Positive Feedback", and "Areas for Improvement".

**CONTEXT PROVIDED:**

---
**1. Project Overview (from README.md/GEMINI.md):**
{readme_content}
---
**2. Recent Commit History (last 15 commits):**
{git_log_content}
---
**3. Project File Tree:**
{file_tree_content}
---
**4. Staged Git Diff (with 10 lines of context):**
{staged_diff_content}
---

**YOUR TASK:**
Based on all the context above, provide a detailed code review in the following Markdown format:

# AI Code Criticism Report

## 1. Overall Assessment
(A one-paragraph summary of the change.)

## 2. Code Quality Score
- **Clarity & Readability:** [Score 1-10]
- **Correctness & Robustness:** [Score 1-10]
- **Style & Consistency:** [Score 1-10]

## 3. Positive Feedback
* (Point 1)
* (Point 2)

## 4. Areas for Improvement
*   **File:** `path/to/file.py`
    *   **Line:** (approximate line number)
    *   **Concern:** (Description of the issue)
    *   **Suggestion:** (How to fix it)
"""

    # 3. Get AI Criticism
    ai_response = get_ai_criticism(system_prompt)

    # 4. Print the report
    print("\n" + "="*80)
    print("                 AI Code Criticism Report")
    print("="*80 + "\n")
    print(ai_response)
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
