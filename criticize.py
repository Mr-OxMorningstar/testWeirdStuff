
import subprocess
import sys
import os
import re

def get_staged_diff():
    """
    Retrieves the staged changes from Git using 'git diff --staged'.

    Returns:
        str: The git diff as a string, or an empty string if there's an error or no diff.
    """
    try:
        result = subprocess.run(
            ['git', 'diff', '--staged'],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            if "not a git repository" in result.stderr:
                print("Error: This is not a Git repository.", file=sys.stderr)
                return None
            print(f"Error getting git diff:\n{result.stderr}", file=sys.stderr)
            return None

        return result.stdout
    except FileNotFoundError:
        print("Error: Git is not installed or not in your PATH.", file=sys.stderr)
        return None

def detect_project_type():
    """
    Detects the project type based on common configuration files.

    Returns:
        str: A string indicating the detected project type (e.g., "TypeScript", "Python", "Unknown").
    """
    if os.path.exists("package.json"):
        for root, _, files in os.walk("."):
            for file in files:
                if file.endswith((".ts", ".tsx")):
                    return "TypeScript"
        return "Node.js"
    elif os.path.exists("requirements.txt") or os.path.exists("pyproject.toml"):
        return "Python"
    return "Unknown"

def parse_diff_for_changed_files(diff_content):
    """
    Parses the git diff content to extract paths of changed files.

    Args:
        diff_content (str): The output from 'git diff --staged'.

    Returns:
        list: A list of file paths that have been changed.
    """
    changed_files = set()
    # Regex to find lines starting with '+++ b/' or '--- a/'
    # which indicate new/old file paths in a diff.
    # We strip '+++ b/' or '--- a/' and any leading 'i/' if present (for index lines).
    for line in diff_content.splitlines():
        match = re.match(r'^\+\+\+ b/(\S+)|^--- a/(\S+)', line)
        if match:
            file_path = match.group(1) or match.group(2)
            if file_path and not file_path.startswith('/dev/null'): # Ignore null devices for added/deleted files
                changed_files.add(file_path)
    return list(changed_files)

def get_file_content(file_path):
    """
    Reads the content of a specified file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file, or None if the file cannot be read.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Warning: Could not read file {file_path}: {e}", file=sys.stderr)
        return None

def main():
    """
    Main function for the criticize agent.
    """
    print("--- Running Criticize Agent ---")

    project_type = detect_project_type()
    print(f"Detected project type: {project_type}")

    staged_diff = get_staged_diff()

    if staged_diff is None:
        print("Could not retrieve staged changes. Exiting.", file=sys.stderr)
        sys.exit(1)

    if not staged_diff.strip():
        print("No staged changes found. Add files to the staging area first with 'git add'.")
        return

    print("\n--- Found Staged Changes ---")
    print(staged_diff)
    print("--------------------------")

    # Gather additional context
    print("\n--- Gathering Context ---")

    # Read GEMINI.md
    gemini_md_content = get_file_content("GEMINI.md")
    if gemini_md_content:
        print("\n--- GEMINI.md Content ---")
        # In a real scenario, this would be summarized or used directly in the prompt
        print(gemini_md_content[:500] + "..." if len(gemini_md_content) > 500 else gemini_md_content)
        print("--------------------------")
    else:
        print("Warning: GEMINI.md not found or could not be read. No project overview context will be provided.")

    # Get content of changed files
    changed_files = parse_diff_for_changed_files(staged_diff)
    if changed_files:
        print("\n--- Content of Changed Files ---")
        for file_path in changed_files:
            file_content = get_file_content(file_path)
            if file_content:
                print(f"\n--- File: {file_path} ---")
                # In a real scenario, this would be summarized or used directly in the prompt
                print(file_content[:500] + "..." if len(file_content) > 500 else file_content)
                print("--------------------------")
    else:
        print("No changed files identified from diff.")

if __name__ == "__main__":
    main()
