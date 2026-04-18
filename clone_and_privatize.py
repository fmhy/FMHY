import os
import subprocess
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of repositories to clone
repositories = [
    "Ph34k/FMHY",
    "Ph34k/edit",
    "Ph34k/.github",
    "Ph34k/dupe-checker",
    "Ph34k/bot",
    "Ph34k/fmhy.github.io",
    "Ph34k/FMHYFilterlist",
    "Ph34k/archive",
    "Ph34k/bookmarks",
    "Ph34k/FMHY-SafeGuard",
    "Ph34k/resources"
]

# GitHub API Details
github_token = 'YOUR_GITHUB_TOKEN'  # Remember to set your GitHub token here
headers = {'Authorization': f'token {github_token}'}

# Clone and privatize function
def clone_and_privatize(repo):
    try:
        # Clone the repository
        logging.info(f'Cloning {repo}...')
        subprocess.run(['git', 'clone', '--mirror', f'https://github.com/{repo}.git'], check=True)
        
        # Change directory into the cloned repository
        repo_name = repo.split('/')[-1]
        os.chdir(repo_name)

        # Push the cloned repository to the new location
        logging.info(f'Pushing {repo_name} to the Ph34k account...')
        subprocess.run(['git', 'push', '--mirror', f'https://github.com/Ph34k/{repo_name}.git'], check=True)
        os.chdir('..')  # Go back to previous directory

        # Setting the repository to private
        response = requests.patch(f'https://api.github.com/repos/Ph34k/{repo_name}', 
                                  headers=headers, 
                                  json={'private': True})
        
        if response.status_code == 200:
            logging.info(f'Successfully set {repo_name} to private.')
        else:
            logging.error(f'Failed to set {repo_name} to private: {response.json()}')
    
    except subprocess.CalledProcessError as e:
        logging.error(f'Error occurred while handling {repo}: {e}')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')

# Run the cloning and privatizing for each repo
for repo in repositories:
    clone_and_privatize(repo)
