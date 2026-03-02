from __future__ import annotations

import config


CONFIG_SECTION = "__ADDON_ID__"

DEFAULTS = {
    "enabled": True,
}

CONFIG_SPEC = {
    "enabled": "boolean(default=True)",
}


def _get_section():
    if CONFIG_SECTION not in config.conf.spec:
        config.conf.spec[CONFIG_SECTION] = dict(CONFIG_SPEC)
    section = config.conf[CONFIG_SECTION]
    for key, value in DEFAULTS.items():
        if key not in section:
            section[key] = value
    return section


def is_enabled() -> bool:
    return bool(_get_section().get("enabled", True))
