"""Security helpers used during application bootstrap."""

from __future__ import annotations

import os
from collections.abc import Mapping


class AdminBootstrapError(RuntimeError):
    """Raised when the first administrator cannot be initialized safely."""


def require_admin_password(environ: Mapping[str, str] | None = None) -> str:
    """Return the configured initial admin password or fail closed.

    The password is intentionally read from the process environment so it is
    not committed to source control or displayed in the repository README.
    """
    source = os.environ if environ is None else environ
    password = source.get("ADMIN_PASSWORD", "").strip()
    if not password:
        raise AdminBootstrapError(
            "ADMIN_PASSWORD must be set before creating the initial administrator"
        )
    return password
