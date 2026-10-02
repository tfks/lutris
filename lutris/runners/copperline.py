"""Runner for Copperline Amiga emulator"""

# Standard Library
import os
import stat
from gettext import gettext as _

# Lutris Modules
from lutris.exceptions import GameConfigError, MissingGameExecutableError
from lutris.runners.runner import Runner
from lutris.util import system
from lutris.util.strings import split_arguments


class copperline(Runner):
    human_name = _("Copperline")
    description = _("Runs Amiga games with the Copperline emulator")
    platform_dict = Runner.to_platform_dict([_("Amiga")])
    entry_point_option = "game_file"

    runner_options = [
        {
            "option": "exe",
            "type": "file",
            "section": _("Game"),
            "label": _("Copperline executable"),
            "help": _("Path to the Copperline AppImage"),
        },
        {
            "option": "args",
            "type": "string",
            "section": _("Game"),
            "label": _("Arguments"),
            "help": _("Additional Copperline command-line arguments"),
        },
        {
            "option": "working_dir",
            "section": _("Game"),
            "type": "directory",
            "label": _("Working directory"),
            "help": _("Defaults to the directory containing the game archive."),
        },
        {
            "option": "full_screen",
            "type": "bool",
            "section": _("UI"),
            "label": _("Full screen"),
            "default": True,
        },
        {
            "option": "hide_statusbar",
            "type": "bool",
            "section": _("UI"),
            "label": _("Hide status bar"),
            "default": True,
        },
        {
            "option": "menu_scale",
            "type": "choice",
            "section": _("UI"),
            "label": _("Menu scale"),
            "default": "1x",
            "choices": [
                ("1x", "1x"),
                ("2x", "2x")
            ]
        },
        {
            "option": "mouse_capture_mode",
            "type": "choice",
            "section": _("Input"),
            "label": _("Mouse capture mode"),
            "default": "click",
            "choices": [
                ("auto", "auto"),
                ("click", "click"),
                ("manual", "manual"),
            ]
        },
        {
            "option": "mouse_sensitivity",
            "type": "range",
            "section": _("Input"),
            "label": _("Mouse sensitivity (0-100)"),
            "default": 50,
            "min": 0,
            "max": 100
        },
        {
            "option": "joystick",
            "type": "choice",
            "section": _("Input"),
            "label": _("Joystick mode"),
            "default": "gamepad",
            "choices": [
                ("gamepad", "gamepad"),
                ("keyboard", "keyboard"),
            ]
        },
        {
            "option": "auto_fire",
            "type": "range",
            "section": _("In-Game"),
            "label": _("Auto fire (0-30)"),
            "default": 0,
            "min": 0,
            "max": 30
        },
        {
            "option": "perf_overlay",
            "type": "bool",
            "section": _("Performance"),
            "label": _("Performance overlay"),
            "default": False
        },
        {
            "option": "run_ahead_frames",
            "type": "range",
            "section": _("Performance"),
            "label": _("Run ahead frames (0-4)"),
            "default": 0,
            "min": 0,
            "max": 4
        },
        {
            "option": "audio_enable",
            "type": "bool",
            "section": _("Audio"),
            "label": _("Audio on/off"),
            "default": True
        },
        {
            "option": "audio_channel",
            "type": "choice",
            "section": _("Audio"),
            "label": _("Audio mono/stereo"),
            "default": "stereo",
            "choices": [
                ("Mono", "mono"),
                ("Stereo", "stereo")
            ],
        },
        {
            "option": "audio_stereo_separation",
            "type": "range",
            "section": _("Audio"),
            "label": _("Audio stereo separation (0%-100%, 0 = mono)"),
            "default": 100,
            "min": 0,
            "max": 100
        },
        {
            "option": "audio_filter",
            "type": "choice",
            "section": _("Audio"),
            "label": _("Audio filter"),
            "default": "auto",
            "choices": [
                ("Auto", "auto"),
                ("On", "on"),
                ("Off", "off")
            ],
        },
        {
            "option": "model",
            "type": "choice",
            "section": _("Emulator"),
            "label": _("Model"),
            "default": "A500",
            "choices": [
                ("A1000", "A1000"),
                ("A500", "A500"),
                ("A500OCS", "A500OCS"),
                ("A500Plus", "A500Plus"),
                ("A600", "A600"),
                ("A1200", "A1200"),
                ("A3000", "A3000"),
                ("A4000", "A4000"),
                ("CDTV", "CDTV"),
                ("CD32", "CD32"),
            ],
            "advanced": True,
        },
        {
            "option": "chipset",
            "type": "choice",
            "section": _("Emulator"),
            "label": _("Chipset"),
            "default": "OCS",
            "choices": [
                ("OCS", "OCS"),
                ("ECS", "ECS"),
                ("AGA", "AGA"),
            ],
            "advanced": True,
        },
        {
            "option": "video",
            "type": "choice",
            "section": _("Emulator"),
            "label": _("Video"),
            "default": "N/A",
            "choices": [
                ("Not set", "N/A"),
                ("PAL", "PAL"),
                ("NTSC", "NTSC"),
            ],
            "advanced": True,
        },
        {
            "option": "cpu",
            "type": "choice",
            "section": _("Emulator"),
            "label": _("CPU"),
            "default": "68000",
            "choices": [
                ("68000", "68000"),
                ("68010", "68010"),
                ("68EC020", "68EC020"),
                ("68020", "68020"),
                ("68030", "68030"),
                ("68040", "68040"),
                ("68060", "68060"),
            ],
            "advanced": True,
        },
        {
            "option": "cpu_clock",
            "type": "range",
            "section": _("Emulator"),
            "label": _("CPU clock (7-50)"),
            "default": 7,
            "min": 7,
            "max": 50,
            "advanced": True,
        },
        {
            "option": "fpu",
            "type": "bool",
            "section": _("Emulator"),
            "label": _("Floating point unit"),
            "default": False,
            "advanced": True,
        },
        {
            "option": "chip",
            "type": "choice",
            "section": _("Emulator"),
            "label": _("Chip memory size"),
            "default": "N/A",
            "choices": [
                ("Not set", "N/A"),
                ("512K", "512K"),
                ("1M", "1M"),
                ("4M", "4M"),
                ("8M", "8M"),
                ("16M", "16M"),
                ("32M", "32M"),
                ("64M", "64M"),
                ("128M", "128M"),
            ],
            "advanced": True,
        },
        {
            "option": "fast",
            "type": "choice",
            "section": _("Emulator"),
            "label": _("Fast memory size"),
            "default": "0M",
            "choices": [
                ("Not set", "0M"),
                ("1M", "1M"),
                ("4M", "4M"),
                ("8M", "8M"),
                ("16M", "16M"),
                ("32M", "32M"),
                ("64M", "64M"),
                ("128M", "128M"),
            ],
            "advanced": True,
        },
        {
            "option": "slow",
            "type": "range",
            "section": _("Emulator"),
            "label": _("Slow memory size (0-512 kB)"),
            "default": 0,
            "min": 0,
            "max": 512,
            "advanced": True,
        },
    ]

    game_options = [
        {
            "option": "game_file",
            "type": "file",
            "label": _("Game archive"),
            "help": _("WHDLoad archive, such as a .lha file"),
        }
    ]

    @property
    def emulator_exe(self):
        exe = self.runner_config.get("exe")
        if not exe:
            return None
        return os.path.expanduser(exe)

    @property
    def game_file(self):
        game_file = self.game_config.get("game_file")
        if not game_file:
            return None

        game_file = os.path.expanduser(game_file)
        if os.path.isabs(game_file):
            return game_file
        if self.game_path:
            return os.path.join(self.game_path, game_file)
        return game_file

    @property
    def working_dir(self):
        configured_dir = self.runner_config.get("working_dir")
        if configured_dir:
            return os.path.expanduser(configured_dir)
        if self.game_file:
            return os.path.dirname(self.game_file)
        return self.game_path

    def is_installed(self, flatpak_allowed: bool = True) -> bool:
        return bool(self.emulator_exe and system.path_exists(self.emulator_exe))

    def get_command(self):
        return [self.emulator_exe] if self.emulator_exe else []

    def play(self):
        emulator = self.emulator_exe
        game_file = self.game_file

        if not emulator or not system.path_exists(emulator):
            raise MissingGameExecutableError(filename=emulator)

        if not game_file or not system.path_exists(game_file):
            raise MissingGameExecutableError(filename=game_file)

        if not os.stat(emulator).st_mode & stat.S_IXUSR:
            raise GameConfigError(_("The Copperline AppImage is not executable: %s") % emulator)

        command = [emulator, "--whdload", game_file]

        if self.runner_config.get("full_screen", True):
            command.append("--full-screen")

        if self.runner_config.get("hide_statusbar", True):
            command.append("--hide-status-bar")

        if self.runner_config.get("perf_overlay"):
            command.append("--perf-overlay")

        if self.runner_config.get("menu_scale") == "2x":
            command.extend(["--menu-scale", "2x"])

        mcm = self.runner_config.get("mouse_capture_mode")

        if not mcm is None and mcm != "click":
            command.extend(["--mouse-capture", mcm])

        ms = self.runner_config.get("mouse_sensitivity")

        if not ms is None and ms != 50:
            command.extend(["--mouse-sensitivity", ms])

        js = self.runner_config.get("joystick")

        if not js is None and js != "gamepad":
            command.extend(["--joystick", js])

        af = self.runner_config.get("auto_fire")

        if not af is None:
            command.extend(["--autofire", str(af)])

        raf = self.runner_config.get("run_ahead_frames")

        if not raf is None:
            command.extend(["--run-ahead", str(raf)])

        audio_enable = self.runner_config.get("audio_enable")

        if not audio_enable is None and audio_enable == False:
            command.append("--noaudio")

        audio_channel_mode = self.runner_config.get("audio_channel_mode")

        if not audio_channel_mode is None and audio_channel_mode == "mono":
            command.extend(["--audio-channel-mode", "mono"])

        audio_stereo_separation = self.runner_config.get("audio_stereo_separation")

        if not audio_stereo_separation is None and audio_stereo_separation != 100:
            command.extend(["--audio-stereo-separation", audio_stereo_separation])

        audio_filter = self.runner_config.get("audio_filter")

        if not audio_stereo_separation is None and audio_filter != "auto":
            command.extend(["--audio-filter", audio_filter])

        audio_filter = self.runner_config.get("audio_filter")

        if not audio_filter is None and audio_filter != "auto":
            command.extend(["audio-filter", audio_filter])

        model = self.runner_config.get("model")

        if not model is None:
            command.extend(["--model", model])

        chipset = self.runner_config.get("chipset")

        if not chipset is None:
            command.extend(["--chipset", chipset])

        video = self.runner_config.get("video")

        if not video is None and video != "N/A":
            command.extend(["--video", video])

        cpu_clock = self.runner_config.get("cpu_clock")

        if not cpu_clock is None and cpu_clock > 0:
            command.extend(["--cpu-clock", str(cpu_clock)])

        if self.runner_config.get("fpu", False):
            command.append("--fpu")

        chip = self.runner_config.get("chip")

        if not chip is None and chip != "N/A":
            command.extend(["--chip", chip])

        fast = self.runner_config.get("fast")

        if not fast is None and fast != "0M":
            command.append("--fast " + fast)

        slow = self.runner_config.get("slow")

        if not slow is None and slow > 0:
            command.append("--slow " + str(slow))

        extra_args = self.runner_config.get("args") or ""
        command.extend(split_arguments(extra_args))

        return {
            "command": command,
            "working_dir": self.working_dir,
        }

