"""
opt-extend
Usage:
  opt-extend authorize <project_id> <token>
  opt-extend list <project_id> [--json]
  opt-extend initialize <project_id> <directory_path> <edit_url> [--description=<description>] [--name=<name>]
  opt-extend upload <extension_directory_path> [--enable]
  opt-extend pull <project_id> <extension_id> <extension_directory_path>
  opt-extend disable <project_id> (--grep=<grep_string> | --extension-id=<extension_id>)
  opt-extend  update <project_id> (--all | --grep=<grep_string> | --extension-id=<extension_id>) (--css-only=<css_file> | <update_directory>)
  opt-extend extension_data <project_id> <extension_id> [--page_id=<page_id>] [--json]
  opt-extend unauthorize ( --project-id=<project_id> | --all )
  opt-extend -h w| --help
  opt-extend --version
Options:
  -h --help                         Show this screen.
  --version                         Show version.
Examples:
  opt-extend list_extensions
Help:
  For help using this tool, please open an issue on the Github repository: www.github.com/JohannaGoergen/optimizely-extensions-cli
"""

import asyncio
from inspect import getmembers, isclass

from docopt import docopt
import opt_extend.commands

from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=VERSION)
    loop = asyncio.get_event_loop()
    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(opt_extend.commands, k) and v:
            module = getattr(opt_extend.commands, k)
            opt_extend.commands = getmembers(module, isclass)
            command = [command[1] for command in opt_extend.commands if command[0] != 'Base'][0]
            command = command(options)
            loop.run_until_complete(command.run())
    loop.close()
