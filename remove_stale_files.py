import os
from datetime import datetime, timedelta
from github import Github

# Replace with your GitHub access token
ACCESS_TOKEN = os.environ.get('TEST_REMOVE_STALE_FILES_PIPELINE_SECRET')

# Replace with your repository information
REPO_OWNER = 'OktayGardener'
REPO_NAME = 'remove-stale-files'

# Authenticate with GitHub
g = Github(ACCESS_TOKEN)
repo = g.get_user(REPO_OWNER).get_repo(REPO_NAME)

# Set up a test file that hasn't been modified in two days
for i in range(0,5):
    test_file_path = 'test-file-' + i + '.md'
    test_file_content = 'This is a test file'
    if i < 2:
        test_file_last_modified = datetime.utcnow() - timedelta(days=2)

# Create the test file
    repo.create_file(test_file_path, "test commit", test_file_content)

# Set the "last_modified" property of the test file to two days ago
    test_file = repo.get_contents(test_file_path)
    if i < 2:
        repo.update_file(test_file_path, "test commit", test_file_content, test_file.sha, last_modified=test_file_last_modified)

# Get a list of all Markdown files in the repository
markdown_files = [f for f in repo.get_contents("") if f.name.endswith(".md")]
print("markdown files: ")
print(markdown_files)

# Iterate over each file and delete it if it hasn't been modified in two days
for file in markdown_files:
    if file.last_modified < test_file_last_modified:
        repo.delete_file(file.path, "Removing stale file", file.sha)