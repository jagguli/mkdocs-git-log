from mkdocs.plugins import BasePlugin
import os
import subprocess
import logging

logger = logging.getLogger(__file__)


class GitLogPlugin(BasePlugin):
    def on_page_context(self, context, page, config, nav, **kwargs):
        logger.info(f"generating gitlog for {page}")
        context["git_page_logs"] = git_log(page, config["docs_dir"])
        return context


def git_log(page, docs_dir):
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

    return f"""
<details>
  <summary>
    Git log for current page [{page.file.src_path}]
  </summary>
  <p>
    {table_html}
  </p>
</details>
"""
