"""
`ytube_api` commandline interface.

## Usage:

```sh
$ python -m ytube_api --help
# or
$ ytube --help
```

## Download video

```sh
$ ytube download <QUERY : video title or url>
# e.g
$ ytube download "Alan walker alone"
```

## Download only audio
```sh
$ ytube download <QUERY : video title or url> --mp3
# e.g
$ ytube download https://youtu.be/1-xGerv5FOk?si=5Jg8nABSf8SWlUmO --mp3
```

## Get query suggestions

```sh
$ ytube suggest <QUERY: text>
# e.g
$ ytube suggest "Alan Walker official music video"
```


## Interactive mode

- Features live-search

```sh
$ ytube interactive

# Welcome to interactive ytube. Type 'help' or 'h' for usage info.
# Submit any bug at https://github.com/Simatwa/ytube/issues/new
# ╭─[Smartwa@YTUBE]~[🕒18:25:19-💻00:00:00-⚡0.0s] 
# ╰─>
```
"""

import click
import cmd
import os
import sys
import time
import getpass
import datetime
from colorama import Fore
from rich.table import Table
from rich.console import Console
import ytube_api.constants as const
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import ThreadedCompleter, Completer, Completion
from prompt_toolkit.document import Document

default_context_settings = dict(auto_envvar_prefix="YTUBE")


@click.group()
@click.version_option(package_name="ytube-api")
def ytube():
    """Download YouTube videos in mp4 and mp3 formats"""


@ytube.command(context_settings=default_context_settings)
@click.argument("query")
@click.option(
    "-q",
    "--quality",
    type=click.Choice(const.download_qualities + ("128|720",)),
    help="Media download quality - 128|720",
    default="128|720",
)
@click.option(
    "--mp4/--mp3", default=True, help="Download audio (mp3) or video (mp4) - mp4"
)
@click.option(
    "--enable-progressbar/--disable-progressbar",
    default=True,
    help="Show or hide progressbar",
)
@click.option(
    "-l",
    "--limit",
    type=click.INT,
    help="Total number of items to be downloaded that matched the search - 1",
    default=1,
)
@click.option(
    "-t",
    "--timeout",
    type=click.INT,
    help="Http request timeout - 20",
    default=20,
)
@click.option(
    "-c",
    "--channels",
    help="Download videos posted by this channel titles - None.",
    metavar="Name",
    multiple=True,
)
@click.option(
    "-d",
    "--dir",
    help="Directory for saving the contents to - pwd.",
    type=click.Path(exists=True, file_okay=False),
    default=os.getcwd(),
)
@click.option("-o", "--output", help="Filename to save the contents under - None")
@click.option(
    "-b",
    "--busy-bar",
    help="Busy bar index - ['', '/','■█■■■', '⡿'] - 2",
    default=2,
    type=click.IntRange(
        min=0,
        max=3,
    ),
)
@click.option("--quiet", is_flag=True, help="Do not stdout informative messages")
@click.option("--resume", is_flag=True, help="Resume incomplete download")
@click.option(
    "--confirm", is_flag=True, help="Ask user for permission to download a video/audio"
)
@click.option(
    "--play",
    is_flag=True,
    help="Play the video/audio after completing download process",
)
@click.option(
    "--experiment", is_flag=True, help="Enable features that are known to be buggy"
)
def download(
    query,
    quality,
    mp4,
    enable_progressbar,
    limit,
    timeout,
    channels,
    dir,
    output,
    busy_bar,
    quiet,
    resume,
    confirm,
    play,
    experiment,
):
    """Search and download video in mp4 or mp3 formats"""
    from ytube_api import Auto

    saved_to = Auto(
        query=query,
        format="mp4" if mp4 else "mp3",
        limit=limit,
        confirm=confirm,
        quality=quality,
        timeout=timeout,
        spinner_index=busy_bar,
        channels=channels,
        filename=output,
        dir=dir,
        quiet=quiet,
        resume=resume,
        progress_bar=enable_progressbar,
        experiment=experiment,
    )
    if not quiet and saved_to:
        print(
            "## Saved to : \n" + "\n".join([str(path) for path in saved_to])
            if isinstance(saved_to, list)
            else "## Saved to : " + str(saved_to)
        )
        if play:
            path_to_file = saved_to[0] if isinstance(saved_to, list) else saved_to
            click.launch(str(path_to_file))


class CustomCompleter(Completer):
    """Suggests video based on user query"""

    def __init__(
        self,
        yt: object,
        caller: object,
        suggestions_limit: int = 5,
        special_commands: list[str] = [],
    ):
        self.suggestions_limit = suggestions_limit
        self.yt = yt
        self.caller = caller
        self.special_commands = special_commands

    def get_completions(self, document: Document, complete_event):
        word = document.text
        if word and self.suggestions_limit > 0 and not word.startswith("./"):
            completions = []
            first_word = word.split(" ")[0]
            if first_word in self.special_commands:
                completions.append(
                    Completion(
                        f"{first_word} [RESERVED] "
                        + getattr(self.caller, f"do_{first_word}").__doc__
                    )
                )
                return completions
            for count, suggestion in enumerate(self.yt.suggest_queries(word), start=1):
                completions.append(Completion(suggestion, start_position=-len(word)))
                if count >= self.suggestions_limit:
                    break
            return completions
        return []


class Interactive(cmd.Cmd):
    """Perform live search and download video in mp3/mp4 formats interactively"""

    intro = (
        "Welcome to interactive ytube. "
        "Type 'help' or 'h' for usage info.\n"
        f"Submit any bug at https://github.com/Simatwa/ytube/issues/new"
    )
    __init_time = time.time()

    def __init__(
        self,
        quality,
        limit,
        timeout,
        busy_bar,
        select,
        confirm,
        dir,
        disable_coloring,
        query=None,
        mp4=True,
        play=False,
        suggestions_limit: int = 10,
        **kwargs,
    ):
        from ytube_api import Ytube, Auto

        super().__init__()
        self.__start_time = time.time()
        self.__end_time = time.time()
        self.yt = Ytube(timeout=timeout, spinner_index=busy_bar)
        self.downloader = Auto

        self.completer_session = PromptSession(
            "",
            completer=ThreadedCompleter(
                CustomCompleter(
                    self.yt,
                    self,
                    suggestions_limit,
                    [
                        "sys",
                        "settings",
                        "mp4",
                        "mp3",
                        "help",
                        "h",
                        "exit",
                        "configure",
                        "clear",
                    ],
                )
            ),
        )
        self.suggestions_limit = suggestions_limit
        self.disable_coloring = disable_coloring
        self.quality = quality
        self.limit = limit
        self.timeout = timeout
        self.busy_bar = busy_bar
        self.dir = dir
        self.select = select
        self.confirm = confirm
        self.play = play

        if kwargs.get("format"):
            self.format = kwargs.get("format")
        else:
            self.format = "mp4" if mp4 else "mp3"

        if query:
            self.default(query)

    @property
    def current_settings(self):
        return dict(
            format=self.format,
            quality=self.quality,
            limit=self.limit,
            timeout=self.timeout,
            busy_bar=self.busy_bar,
            dir=self.dir,
            suggestions_limit=self.suggestions_limit,
            select=self.select,
            confirm=self.confirm,
            play=self.play,
            disable_coloring=self.disable_coloring,
        )

    @property
    def prompt(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        def find_range(start, end, hms: bool = False):
            in_seconds = round(end - start, 1)
            return (
                str(datetime.timedelta(seconds=in_seconds)).split(".")[0].zfill(8)
                if hms
                else in_seconds
            )

        if not self.disable_coloring:
            cmd_prompt = (
                f"╭─[`{Fore.CYAN}{getpass.getuser().capitalize()}@YTUBE]`"
                # f"(`{Fore.MAGENTA}{self.get_provider})`"
                f"~[`{Fore.LIGHTWHITE_EX}🕒{Fore.BLUE}{current_time}-`"
                f"{Fore.LIGHTWHITE_EX}💻{Fore.RED}{find_range(self.__init_time, time.time(), True)}-`"
                f"{Fore.LIGHTWHITE_EX}⚡{Fore.YELLOW}{find_range(self.__start_time, self.__end_time)}s]`"
                # f"\n╰─>"
            )
            whitelist = ["[", "]", "~", "-", "(", ")"]
            for character in whitelist:
                cmd_prompt = cmd_prompt.replace(character + "`", Fore.RESET + character)
            return cmd_prompt

        else:
            return (
                f"╭─[{getpass.getuser().capitalize()}@YTUBE]"
                f"~[🕒{current_time}"
                f"-💻{find_range(self.__init_time, time.time(), True)}"
                f"-⚡{find_range(self.__start_time, self.__end_time)}s]"
                # "\n╰─>"
            )

    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline

                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                if hasattr(readline, "backend") and readline.backend == "editline":
                    if self.completekey == "tab":
                        # libedit uses "^I" instead of "tab"
                        command_string = "bind ^I rl_complete"
                    else:
                        command_string = f"bind {self.completekey} rl_complete"
                else:
                    command_string = f"{self.completekey}: complete"
                readline.parse_and_bind(command_string)
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            print(self.prompt, end="")
                            line = self.completer_session.prompt("\n╰─>")
                        except EOFError:
                            line = "EOF"
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = "EOF"
                        else:
                            line = line.rstrip("\r\n")
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline

                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass

    def do_sys(self, line):
        """Execute system commands
        shortcut [./<command>]
        Usage:
            sys <System command>
                  or
             ./<System command>
        """
        os.system(line)

    def do_clear(self, line):
        """Clear console"""
        sys.stdout.write("\u001b[2J\u001b[H")
        sys.stdout.flush()

    def do_h(self, line):
        """Show help info in tabular form"""
        table = Table(
            title="Help info",
            show_lines=True,
        )
        table.add_column("No.", style="white", justify="center")
        table.add_column("Command", style="yellow", justify="left")
        table.add_column("Function", style="cyan")
        command_methods = [
            getattr(self, method)
            for method in dir(self)
            if callable(getattr(self, method)) and method.startswith("do_")
        ]
        command_methods.append(self.default)
        command_methods.reverse()
        for no, method in enumerate(command_methods):
            table.add_row(
                str(no + 1),
                method.__name__[3:] if not method == self.default else method.__name__,
                method.__doc__,
            )
        Console().print(table)

    def do_mp4(self, line):
        """Download video"""
        if not line:
            print("Query is required!")
        else:
            self.default("/" + const.video_download_format + " " + line)

    def do_mp3(self, line):
        """Download audio"""
        if not line:
            print("Query is required!")
        else:
            self.default("/" + const.audio_download_format + " " + line)

    def do_settings(self, line):
        """Check current settings"""
        table = Table(
            title="Current Settings",
            show_lines=True,
        )
        table.add_column("No.", style="white", justify="center")
        table.add_column("Variable", style="yellow", justify="left")
        table.add_column("Value", style="cyan")

        for count, key_value in enumerate(self.current_settings.items(), start=1):
            table.add_row(
                str(count),
                key_value[0],
                str(key_value[1]) if isinstance(key_value[1], int) else key_value[1],
            )
        Console().print(table)

    def do_configure(self, line):
        """Modify settings"""
        new_settings_jar = {}
        types_ = dict(
            format=click.Choice(const.download_formats),
            quality=click.Choice(const.download_qualities),
            busy_bar=click.IntRange(0, 3),
        )
        for key, value in self.current_settings.items():
            new_settings_jar[key] = click.prompt(
                f"> Enter new value for {key} ",
                type=types_.get(key, type(value)),
                default=value,
            )
        self.__init__(**new_settings_jar)
        click.secho("* New settings applied.", fg="cyan")

    def default(self, line):
        """Search videos"""
        if line.startswith("./"):
            self.do_sys(line[2:])

        elif line != "":
            self.__start_time = time.time()
            splitted_lines = line.split(" ")
            if splitted_lines[0] == "/" + const.video_download_format:
                format = const.video_download_format
                quality = (
                    const.default_audio_download_quality
                    if not self.quality in const.video_download_qualities
                    else self.quality
                )
                line = " ".join(splitted_lines[1:])
            elif splitted_lines[0] == "/" + const.audio_download_format:
                format = const.audio_download_format
                quality = (
                    const.default_video_download_quality
                    if not self.quality in const.audio_download_qualities
                    else self.quality
                )
                line = " ".join(splitted_lines[1:])
            else:
                if self.select:
                    format = click.prompt(
                        "Enter format", type=click.Choice(const.download_formats)
                    )
                    quality = click.prompt(
                        "Enter quality",
                        type=click.Choice(const.format_quality_map[format]),
                    )
                else:
                    format = self.format
                    quality = self.quality
            try:
                saved_to = self.downloader(
                    query=line,
                    format=format,
                    quality=quality,
                    confirm=self.confirm,
                    timeout=self.timeout,
                    spinner_index=self.busy_bar,
                )
                if self.play:
                    path_to_file = (
                        saved_to[0] if isinstance(saved_to, list) else saved_to
                    )
                    click.launch(str(path_to_file))
            except Exception as e:
                print(
                    f"> Error occured - {e.args[1] if e.args and len(e.args)>1 else e}"
                )
            self.__end_time = time.time()

    def do_exit(self, line):
        """Quit this program"""
        if click.confirm("Are you sure to exit"):
            click.secho("Okay Goodbye!", fg="yellow")
            return True


class Commands:
    """Commands for various tasks"""

    @click.command(context_settings=default_context_settings)
    @click.argument("query", required=False)
    @click.option(
        "-q",
        "--quality",
        type=click.Choice(const.download_qualities + ("128|720",)),
        help="Media download quality - 128|720",
        default="128|720",
    )
    @click.option(
        "--mp4/--mp3", default=True, help="Download audio (mp3) or video (mp4) - mp4"
    )
    @click.option(
        "-s",
        "--suggestions-limit",
        type=click.INT,
        help="Query suggestions limit - 10",
        default=10,
    )
    @click.option(
        "-l",
        "--limit",
        type=click.INT,
        help="Total number of items to be downloaded that matched the search - 1",
        default=1,
    )
    @click.option(
        "-t",
        "--timeout",
        type=click.INT,
        help="Http request timeout - 20",
        default=20,
    )
    @click.option(
        "-b",
        "--busy-bar",
        help="Busy bar index - ['', '/','■█■■■', '⡿'] - 2",
        default=2,
        type=click.IntRange(
            min=0,
            max=3,
        ),
    )
    @click.option(
        "-d",
        "--dir",
        help="Directory for saving the contents to - pwd.",
        type=click.Path(exists=True, file_okay=False),
        default=os.getcwd(),
    )
    @click.option(
        "--disable-coloring",
        is_flag=True,
        help="Stdout interactive texts in white font color",
    )
    @click.option(
        "--select",
        is_flag=True,
        help="Prompt user download format and quality every time.",
    )
    @click.option(
        "--confirm",
        is_flag=True,
        help="Ask user for permission to download a video/audio",
    )
    @click.option(
        "--play",
        is_flag=True,
        help="Play the video/audio after completing download process",
    )
    def interactive(**kwargs):
        """Search and download videos/audio interactively"""
        Interactive(**kwargs).cmdloop()

    @click.command(context_settings=default_context_settings)
    @click.argument("query")
    @click.option(
        "-l",
        "--limit",
        help="Limit suggestions to this amount - 30",
        type=click.IntRange(1, 100),
        default=30,
    )
    @click.option(
        "-t",
        "--timeout",
        help="Http request timeout - 20",
        type=click.INT,
        default=20,
    )
    @click.option("--json", is_flag=True, help="Stdout suggestion in json format")
    def suggest(query, limit, timeout, json):
        """Suggest videos based on your query"""
        from ytube_api import Ytube

        suggestions = Ytube(timeout).suggest_queries(query)
        if len(suggestions) > limit:
            suggestions = suggestions[:limit]

        import rich

        if json:
            rich.print_json(data=dict(suggestions=suggestions))
        else:
            table = Table(title=f'Suggestions for "{query}"', show_lines=True)
            table.add_column("No.", justify="center", style="white")
            table.add_column("Suggestion", justify="left", style="cyan")
            for count, suggestion in enumerate(suggestions, start=1):
                table.add_row(str(count), suggestion)
            rich.print(table)


def main():
    try:
        ytube.add_command(Commands.interactive)
        ytube.add_command(Commands.suggest)
        if len(sys.argv) == 1:
            # Just a hack to make 'interactive' default command
            sys.argv.append("interactive")
        ytube()
    except Exception as e:
        print(
            f"> Error occured - {e.args[1] if e.args and len(e.args)>1 else e}. \nQuitting."
        )
        from sys import exit

        exit(1)
