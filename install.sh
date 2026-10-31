#!/usr/bin/env bash
# Orbit Translate installer.
#
# Copies the entry and the orbit_translate/ package into ~/.config/noctalia/tools/,
# the same place Nyxuri deploys them, so both install paths stay interchangeable.
# The user config orbit-translate__custom__.toml is copied only when missing and
# is never overwritten or removed.
#
#   ./install.sh               install or refresh program files
#   ./install.sh --uninstall   remove program files, keep the user config
set -euo pipefail

if [ "$(id -u)" -eq 0 ]; then
    printf 'Do not run install.sh as root.\n' >&2
    exit 1
fi

src="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
dest="$HOME/.config/noctalia/tools"
entry="orbit-translate.py"
package="orbit_translate"
config="orbit-translate__custom__.toml"

remove_files() {
    rm -f -- "$dest/$entry"
    rm -rf -- "${dest:?}/$package"
    printf 'Removed program files from %s\n' "$dest"
    if [ -e "$dest/$config" ]; then
        printf 'Kept user config: %s\n' "$dest/$config"
    fi
}

install_files() {
    mkdir -p -- "$dest"
    stage="$(mktemp -d "$dest/.orbit-translate.XXXXXX")"
    trap 'rm -rf -- "$stage"' EXIT

    # Stage first, then rename into place: a crash never leaves a half-copied package.
    cp -R -- "$src/$package" "$stage/$package"
    find "$stage/$package" -name '__pycache__' -type d -prune -exec rm -rf -- {} +
    find "$stage/$package" -name '*.py[cod]' -type f -delete
    install -m 0755 -- "$src/$entry" "$stage/$entry"

    if [ -d "$dest/$package" ]; then
        mv -- "$dest/$package" "$stage/$package.old"
    fi
    mv -- "$stage/$package" "$dest/$package"
    mv -f -- "$stage/$entry" "$dest/$entry"

    if [ ! -e "$dest/$config" ]; then
        install -m 0644 -- "$src/config/$config" "$dest/$config"
        printf 'Created user config: %s\n' "$dest/$config"
    fi
    printf 'Installed entry: %s\n' "$dest/$entry"
    printf 'Check dependencies: %s --check-deps\n' "$dest/$entry"
}

case "${1:-}" in
    "") install_files ;;
    --uninstall) remove_files ;;
    *)
        printf 'Usage: %s [--uninstall]\n' "$0" >&2
        exit 2
        ;;
esac
