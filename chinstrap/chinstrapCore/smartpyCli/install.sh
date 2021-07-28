#!/usr/bin/env bash

set -e

export FORCE_COLOR=1

say () {
    {
        printf "[SmartPyInstaller] "
        printf "$@"
        printf "\n"
    } >&2
}

export smartml_app_name=install.sh
install_path=$(dirname "$0")
export smartpy_install_path="$install_path"

usage () {
    cat >&2 <<EOF
[SmartPyInstaller]

See introduction: https://smartpy-io.medium.com/f5bd8772b74a

Install directory: $install_path

Usage: $(basename $0) <command> <arguments>

- local-install PATH                   : Install the default version of SmartPy at PATH.
- local-install-custom DISTRIB PATH    : Like local-install but get the 'DISTRIB' version.
- local-install-from SRC-PATH DST-PATH :
  Install from another installation, or from the git repository's python/
  directory.

EOF
}

download () {
    local uri="$1"
    local out="$2"
    say "Downloading $uri to $out ..."
    if [ -f "$out" ] ; then
        rm "$out"
    fi
    curl --fail --show-error -s "$uri" > "$out"
    if [ -f "$out" ] ; then
        :
    else
        say "Download of '$uri' failed"
        exit 4
    fi
}

files_to_install="
originator.js
SmartPy.sh
asciidoctor.css
browser.py
coderay-asciidoctor.css
install.sh
reference.css
reference.html
smart.css
smart.js
smartpy.py
smartpyc.js
smartpyc.py
smartpyio.py
templates/welcome.py
theme.js
typography.css
"

install_from () {
    local method="$1"
    local from="$2"
    local path="$3"

    if [ "$path" = "" ]; then
        echo "Install in default directory: ~/smartpy-cli ? [y/N] "
        read default_install
        if [ "$default_install" = "y" ]; then
            path=~/smartpy-cli
        else
            echo "Cancelling"
            exit 1
        fi
    fi

    if [ -d "$path" ]; then
        echo "Directory ${path} already exists."
        echo "Files will be directly created in ${path}; overwrite ? [y/N] "
        read overwrite
        if [ "$overwrite" != "y" ]; then
            echo "Cancelling"
            exit 1
        fi
    fi

    mkdir -p $path/scripts
    mkdir -p $path/templates
    for f in $files_to_install ; do
        $method "$from/$f" "$path/$f"
    done
    if [ "$native" = "1" ]; then
        $method "$from/smartpyc" "$path/smartpyc"
        chmod +x "$path/smartpyc"
    fi
    ( cd "$path" ;
      npm init --yes > /dev/null ;
      npm install libsodium-wrappers-sumo bs58check js-sha3 tezos-bls12-381 chalk @smartpy/originator ; )
    chmod +x "$path/SmartPy.sh" "$path/originator.js"
    say "Installation successful in $path"
}

native=0
for var in "$@"
do
    case "$var" in
        "--native")
            native=1;;
        * )
        ;;
    esac
done

case "$1" in
    "help" | "--help" | "-h")
        usage ;;
    "" | "local-install" | "--native")
        install_from download https://smartpy.io/cli "$2" ;;
    "local-install-custom" )
        install_from download "$2" "$3" ;;
    "local-install-from" )
        shift
        install_from cp "$1" "$2" ;;
    * )
        usage
        ;;
esac
