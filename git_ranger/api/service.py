from github import Github

# or using an access token

class Service:

    def __init__(self, accesstoken):
        self.accesstoken = accesstoken

    """Return status of a single pr. """
    def get_pr_data(self, org, repo, pr):
        pr_list = {}
        pr_data = []
        try:
            g = Github(self.accesstoken)
            repo = g.get_repo(org + "/" + repo)
            pr = repo.get_pull(int(pr))
            branch_name = pr.base.label.split(":")[1]
            branch = repo.get_branch(branch_name)
            if branch.protected:
                pr_data.append(self.process_pr_data(repo, pr, branch, True))
            else:
                pr_data.append(self.process_pr_data(repo, pr, branch, False))
            pr_list[repo.name] = {"prs": pr_data}
        except Exception as e:
            return e
        return pr_list

    """Return status of every PR status check"""
    @staticmethod
    def get_pr_status(pr, commit_status):
        pr_list = {}
        if commit_status.lower() == "pending":
            pr_list["id"] = pr.number
            pr_list["state"] = "STATUS_CHECK_PENDING"
        elif commit_status.lower() == "failure":
            pr_list["id"] = pr.number
            pr_list["state"] = "FAILING"
        elif commit_status.lower() == "success":
            pr_list["id"] = pr.number
            pr_list["state"] = "MERGE_PENDING"
        return pr_list

    """Process every pr and return it's status"""
    def process_pr_data(self, repo, pr, branch, protected=False):
        pr_list = {}
        try:
            if pr.state.lower() == "closed":
                pr_list["id"] = pr.number
                pr_list["state"] = "CLOSED"
            else:
                review_requests = pr.get_review_requests()
                reviews = list(pr.get_reviews())
                sha = pr.head.sha
                commit = repo.get_commit(sha=sha)
                commit_status = commit.get_combined_status().state
                if protected:
                    if branch.get_protection().required_pull_request_reviews is not None:
                        required_approving_review_count = branch.get_required_pull_request_reviews(). \
                                                            required_approving_review_count
                    else:
                        required_approving_review_count = 0
                    if (len(list(review_requests[0])) == 0) and (required_approving_review_count >= 1):
                        pr_list["id"] = pr.number
                        pr_list["state"] = "REVIEWER_PENDING"
                    elif (len(list(review_requests[0])) == 0) and (required_approving_review_count == 0):
                        pr_list.update(self.get_pr_status(pr, commit_status))
                    elif (branch.get_protection().required_status_checks is not None) and \
                            (required_approving_review_count == 0):
                        pr_list.update(self.get_pr_status(pr, commit_status))
                    else:
                        count = 0
                        for review in reviews:
                            if review.state == "APPROVED":
                                count += 1
                            if count >= required_approving_review_count:
                                pr_list.update(self.get_pr_status(pr, commit_status))
                        if count < required_approving_review_count:
                            pr_list["id"] = pr.number
                            pr_list["state"] = "REVIEW_IN_PROGRESS"
                else:
                    pr_list.update(self.get_pr_status(pr, commit_status))
        except Exception as e:
            return e
        return pr_list

    """Loop through each pull request. """
    def get_pr_values(self, repo):
        pr_data = []
        pr_count = 0
        try:
            pulls = repo.get_pulls(state='open')
            for pr in pulls:
                if pr_count <= 20:
                    branch_name = pr.base.label.split(":")[1]
                    branch = repo.get_branch(branch_name)
                    if branch.protected:
                        pr_data.append(self.process_pr_data(repo, pr, branch, True))
                    else:
                        pr_data.append(self.process_pr_data(repo, pr, branch, False))
                else:
                    break
        except Exception as e:
            return e
        return pr_data

    """Loop through each repository. """
    def get_pr_list(self, org=None, repo=None):
        g = Github(self.accesstoken)
        prs = {}
        repo_count = 0
        try:
            if repo is None:
                for repo in g.get_user().get_repos():
                    prs[repo.name] = {}
                    repo_count += 1
                    if repo_count <= 50:
                        prs[repo.name] = { "prs": self.get_pr_values(repo)}
                    else:
                        break
            else:
                repo = g.get_repo(org+"/"+repo)
                prs[repo.name] = {"prs": self.get_pr_values(repo)}
        except Exception as e:
            return e
        return prs

    """List of repositories. """
    def get_repo_list(self):
        g = Github(self.accesstoken)
        repo_list = {}
        repo_data = []
        try:
            for repo in g.get_user().get_repos():
                repo_data.append(repo.full_name)
            repo_list["repositories"] = repo_data
        except Exception as e:
            return e
        return repo_list

    """ List of pull requests in a repository. """
    def get_pull_list(self, org, repo):
        g = Github(self.accesstoken)
        pull_list = {}
        pull_data = []
        try:
            repo = g.get_repo(org + "/" + repo)
            pulls = repo.get_pulls(state='open')
            for pull in pulls:
                pr = dict()
                pr['id'] = pull.number
                pr['title'] = pull.title
                pull_data.append(pr)
            pull_list["prs"] = pull_data
        except Exception as e:
            return e
        return pull_list

