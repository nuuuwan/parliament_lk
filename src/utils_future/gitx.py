import os
import shutil


class Git:
    @staticmethod
    def run(cmd_list):
        os.system(' && '.join(cmd_list))

    def __init__(self, url_git, branch_name, dir_git):
        self.url_git = url_git
        self.branch_name = branch_name
        self.dir_git = dir_git

    @property
    def cmd_cd(self):
        return f'cd {self.dir_git}'

    def clone_and_checkout(self):
        self.cleanup()

        Git.run([
            f'git clone {self.url_git} {self.dir_git}',
            self.cmd_cd,
            f'git checkout {self.branch_name}',
        ])

    def stage_commit_and_push(self, message):
        Git.run([
            self.cmd_cd,
            'git add .',
            f'git commit -m "{message}"',
            f'git push origin {self.branch_name}',
        ])

    def cleanup(self):
        if os.path.exists(self.dir_git):
            shutil.rmtree(self.dir_git)
