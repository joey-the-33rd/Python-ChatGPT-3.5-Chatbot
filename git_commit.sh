#!/bin/bash

# Script to add all changes, commit grouped changes with meaningful messages, and push to origin main
# Groups files by top-level directory or file extension for meaningful commits
# Improved version with error handling and checks for no changes, including untracked files
# Limits commit to MAX_FILES files per run

MAX_FILES=30

# Get list of modified files
modified_files=$(git status --porcelain | grep -E '^[ M]' | awk '{print $2}')

# Get list of untracked files
untracked_files=$(git ls-files --others --exclude-standard)

# Combine modified and untracked files
files="$modified_files
$untracked_files"

# Remove empty lines
files=$(echo "$files" | sed '/^$/d')

# Limit to MAX_FILES
files_to_commit=$(echo "$files" | head -n $MAX_FILES)

# Check if there are any changes
if [ -z "$files_to_commit" ]; then
  echo "No changes to commit."
  exit 0
fi

commit_count=0
fail_count=0

# Function to commit a group of files with a message
commit_group() {
  local group_files="$1"
  local message="$2"
  echo "$group_files" | xargs git add
  if git commit -m "$message"; then
    echo "Committed group: $message"
    commit_count=$((commit_count + 1))
  else
    echo "Failed to commit group: $message"
    fail_count=$((fail_count + 1))
  fi
}

# Group files by top-level directory or file extension
declare -A groups

while IFS= read -r file; do
  # Extract top-level directory or file extension
  if [[ "$file" == */* ]]; then
    group="${file%%/*}"
  else
    ext="${file##*.}"
    group="ext_$ext"
  fi
  groups["$group"]+="$file"$'\n'
done <<< "$files_to_commit"

# Commit each group with a meaningful message
for group in "${!groups[@]}"; do
  group_files="${groups[$group]}"
  if [[ "$group" == ext_* ]]; then
    ext="${group#ext_}"
    message="Update files with extension .$ext"
  else
    message="Update files in directory $group"
  fi
  commit_group "$group_files" "$message"
done

# Push commits to origin main
if ! git push origin main; then
  echo "Failed to push to origin main"
  exit 1
fi

echo "All changes processed."
echo "Total files committed successfully: $commit_count"
echo "Total files failed to commit: $fail_count"
echo "Committed up to $MAX_FILES files in this run. Run the script again to commit remaining changes."
