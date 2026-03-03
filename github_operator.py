import os
from github import Github
from github.GithubException import GithubException

class GitOperator:
    def __init__(self, token, repo_name):
        self.g = Github(token)
        self.repo = self.g.get_repo(repo_name)

    def create_fix_pr(self, branch_name, file_path, new_content, commit_message, pr_title, pr_body):
        try:
            source_branch = self.repo.default_branch
            source_branch_ref = self.repo.get_branch(source_branch)

            self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch_ref.commit.sha)
            print(f"[*] Created new branch: {branch_name}")

            file = self.repo.get_contents(file_path, ref=source_branch)

            self.repo.update_file(
                path=file.path,
                message=commit_message,
                content=new_content,
                sha=file.sha,
                branch=branch_name
            )
            print(f"[*] Committed changes to: {file_path}")

            pr = self.repo.create_pull(
                title=pr_title,
                body=pr_body,
                head=branch_name,
                base=source_branch
            )
            print(f"[+] Success! Pull Request created at: {pr.html_url}")

        except GithubException as e:
            print(f"[-] GitHub API Error: {e}")

if __name__ == "__main__":
    TOKEN = os.getenv("GITHUB_TOKEN") 
    REPO_NAME = "your-username/Suture-CI"
    
    if TOKEN:
        agent = GitOperator(TOKEN, REPO_NAME)
        print("GitOperator successfully initialized!")
    else:
        print("Notice: GITHUB_TOKEN environment variable is not set yet.")