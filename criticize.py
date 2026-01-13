
import subprocess
import sys

def get_staged_diff():
    """
    Retrieves the staged changes from Git using 'git diff --staged'.

    Returns:
        str: The git diff as a string, or an empty string if there's an error or no diff.
    """
    try:
        # The '--quiet' flag is used to suppress "Not a git repository" errors if run outside a git repo.
        # However, we want to know if it's not a repo, so we'll handle that explicitly.
        result = subprocess.run(
            ['git', 'diff', '--staged'],
            capture_output=True,
            text=True,
            check=False  # Don't raise an exception for non-zero exit codes
        )
        if result.returncode != 0:
            # Handle cases where git command fails (e.g., not a git repo)
            if "not a git repository" in result.stderr:
                print("Error: This is not a Git repository.", file=sys.stderr)
                return None
            print(f"Error getting git diff:\n{result.stderr}", file=sys.stderr)
            return None

        return result.stdout
    except FileNotFoundError:
        print("Error: Git is not installed or not in your PATH.", file=sys.stderr)
        return None

def main():
    """
    Main function for the criticize agent.
    """
    print("--- Running Criticize Agent ---")
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

if __name__ == "__main__":
    main()
