#!/usr/bin/python3
"""creates a .tgz archive from
contents in the web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Creates a .tgz archive from the contents of
    folder.
    Returns:
        str: Path to the created archive otherwise
        None
    """
    local("mkdir -p versions")
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d%H%M%S")
    arch_f = "web_static_" + formatted_date + ".tgz"
    result = local(f"tar -czvf versions/{arch_f} web_static")
    if result.failed:
        return None
    else:
        return "versions/" + arch_f
