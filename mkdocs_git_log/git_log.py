from mkdocs.plugins import BasePlugin
import os
import subprocess


class GitLogPlugin(BasePlugin):
    def on_page_context(self, context, page, config, nav, **kwargs):
        context["git_page_logs"] = git_log(page)
        return context


def git_log(page):
    print(os.getcwd())
    print(page.file.src_path)
    cmd = [
        "git",
        "log",
        "--pretty=format:%h,%an,%ad,%s",
        "--date=short",
        "--",
        os.path.join("mkdocs", page.file.src_path),
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    if result.returncode != 0:
        print(f"error {result.stdout}")
        return ""
    log_output = result.stdout.strip().split("\n")

    table_rows = [
        "<tr><th>Hash</th><th>Author</th><th>Date</th><th>Message</th></tr>"
    ]
    for line in log_output:
        parts = line.split(",")
        table_rows.append(
            "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                *parts
            )
        )
    table_html = "<table>{}</table>".format("\n".join(table_rows))
    return table_html
