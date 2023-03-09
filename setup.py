from setuptools import setup

setup(
    name="mkdocs-git-log",
    version="0.1",
    description="MkDocs plugin to show git log for the current file",
    packages=["mkdocs_git_log"],
    entry_points={
        "mkdocs.plugins": ["git-log = mkdocs_git_log.git_log:GitLogPlugin"]
    },
)
