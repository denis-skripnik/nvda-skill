from __future__ import annotations

import argparse
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"


def _read_template(name: str) -> str:
    return (TEMPLATES_DIR / name).read_text(encoding="utf-8")


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _render(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text


def _resolve_output_dir(raw_output_dir: str) -> Path:
    output_dir = Path(raw_output_dir)
    if output_dir.is_absolute():
        return output_dir.resolve()

    resolved_output_dir = (SKILL_DIR / output_dir).resolve()
    try:
        resolved_output_dir.relative_to(SKILL_DIR)
    except ValueError as error:
        raise ValueError(
            "Relative output_dir must stay inside the skill directory. "
            "Use an absolute path to generate a project elsewhere."
        ) from error
    return resolved_output_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap an NVDA add-on project.")
    parser.add_argument("output_dir")
    parser.add_argument("addon_id")
    parser.add_argument("summary")
    parser.add_argument("--description", default="Adds one concrete NVDA feature.")
    parser.add_argument("--author", default="Author Name")
    parser.add_argument("--url", default="https://example.invalid")
    parser.add_argument("--gesture", default="nvda+shift+t")
    parser.add_argument("--script-description", default="Run the main action")
    parser.add_argument(
        "--advanced",
        action="store_true",
        help="Generate the advanced global plugin and list manager dialog templates.",
    )
    args = parser.parse_args()

    try:
        output_dir = _resolve_output_dir(args.output_dir)
    except ValueError as error:
        parser.error(str(error))
    mapping = {
        "__ADDON_ID__": args.addon_id,
        "__SUMMARY__": args.summary,
        "__DESCRIPTION__": args.description,
        "__AUTHOR__": args.author,
        "__URL__": args.url,
        "__GESTURE__": args.gesture,
        "__SCRIPT_DESCRIPTION__": args.script_description,
    }

    plugin_template = "advanced_global_plugin.py" if args.advanced else "global_plugin_init.py"

    _write_file(output_dir / "buildVars.py", _render(_read_template("buildVars.py"), mapping))
    _write_file(output_dir / "manifest.ini.tpl", _read_template("manifest.ini.tpl"))
    _write_file(output_dir / "build_addon.py", _read_template("build_addon.py"))
    _write_file(
        output_dir / "addon" / "globalPlugins" / args.addon_id / "__init__.py",
        _render(_read_template(plugin_template), mapping),
    )
    _write_file(
        output_dir / "addon" / "globalPlugins" / args.addon_id / "configuration.py",
        _render(_read_template("configuration.py"), mapping),
    )
    _write_file(
        output_dir / "addon" / "globalPlugins" / args.addon_id / "settings.py",
        _render(_read_template("settings_panel.py"), mapping),
    )
    if args.advanced:
        _write_file(
            output_dir / "addon" / "globalPlugins" / args.addon_id / "dialogs.py",
            _render(_read_template("list_manager_dialog.py"), mapping),
        )
    _write_file(
        output_dir / "addon" / "doc" / "en" / "readme.md",
        _render(_read_template("readme.md"), mapping),
    )
    _write_file(
        output_dir / "addon" / "doc" / "en" / "readme.html",
        _render(_read_template("readme.html"), mapping),
    )

    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
