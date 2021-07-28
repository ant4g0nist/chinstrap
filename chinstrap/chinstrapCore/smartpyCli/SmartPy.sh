#!/usr/bin/env bash

set -e

VERSION="0.6.11-1"
export FORCE_COLOR=1

export smartml_app_name=SmartPy.sh

install_path=$(dirname "$0")
export smartpy_install_path="$install_path"

usage () {
    echo "Usage:"
    echo "   $0 test        <script> <output> <options>* (execute all test targets)"
    echo "   $0 compile     <script> <output> <options>* (execute all compilation targets)"
    echo "   $0 kind <kind> <script> <output> <options>* (execute all custom targets added by sp.add_target(..., kind=<kind>))"
    echo "   $0 originate-contract --code <file>(.json|.tz) --storage <file>(.json|.tz) --rpc <rpc-url> [--priate-key edsk...]"
    echo
    echo "   Parameters:"
    echo "         <script>                                 : a python script containing SmartPy code"
    echo "         <output>                                 : a directory for the results"
    echo "         <kind>                                   : a custom target kind"
    echo
    echo "   Options:"
    echo "         --purge                                  : optional, clean output_directory before running"
    echo "         --html                                   : optional, add html logs and outputs"
    echo "         --protocol <delphi|edo|florence|granada> : optional, select target protocol - default is florence"
    echo "         --<flag> <arguments>                     : optional, set some flag with arguments"
    echo "         --<flag>                                 : optional, activate some boolean flag"
    echo "         --no-<flag>                              : optional, deactivate some boolean flag"
    echo "         --mockup                                 : optional, run in mockup (experimental, needs installed source)"
    echo "         --sandbox                                : optional, run in sandbox (experimental, needs installed source)"
}


protocol=PsFLorenaUUuikDWvMDr6fGBRG8kt3e3D3fHoXK1j1BFRxeSH4i

native=no
has_mockup=no
has_sandbox=no
args="$@"
set --
for arg in $args
do
    if [[ "$arg" == --native ]]; then
        native=yes
    elif [[ "$arg" == --no-native ]]; then
        native=no
    elif [[ "$arg" == --mockup ]]; then
        has_mockup=yes
    elif [[ "$arg" == --sandbox ]]; then
        has_sandbox=yes
    elif [[ "$arg" == edo ]]; then
        protocol=PtEdo2ZkT9oKpimTah6x2embF25oss54njMuPzkJTEi5RqfdZFA
        set -- "$@" "$arg"
    elif [[ "$arg" == florence ]]; then
        protocol=PsFLorenaUUuikDWvMDr6fGBRG8kt3e3D3fHoXK1j1BFRxeSH4i
        set -- "$@" "$arg"
    elif [[ "$arg" == granada ]]; then
        protocol=ProtoALphaALphaALphaALphaALphaALphaALphaALphaDdp3zK
        set -- "$@" "$arg"
    else
        set -- "$@" "$arg"
    fi
done


if [[ "$native" == yes ]]; then
    smartpyc="$install_path/smartpyc"
else
    smartpyc="node --stack-size=4096 $install_path/smartpyc.js"
fi

action=none
case "$1" in
    "" | "help" | "--help" | "-h")
        usage
        action=exit
        ;;
    --version)
        echo "SmartPy Version: $VERSION"
        action=exit
        ;;
    # Aliases to cli-js commands:
    # If you add more, please update Meta.smartpy_dot_sh_aliases
    # in smartML/cli_js/node_main.ml
    "compile")
        [ "$#" -lt 3 ] && { usage; exit 1; }
        action=regular
        kind=compilation
        shift
        ;;
    "test")
        [ "$#" -lt 3 ] && { usage; exit 1; }
        action=regular
        kind=test
        shift
        ;;
    "kind")
        [ "$#" -lt 4 ] && { usage; exit 1; }
        action=regular
        kind="$2"
        shift 2
        ;;
    "misc")
        shift
        $smartpyc --install $install_path --misc "$@"
        action=exit
        ;;
    "originate-contract")
        "$(dirname $0)/originator.js" "$@"
        action=exit
        ;;
    * )
        ;;
esac

case $action in
    "none" )
        echo "SmartPy.sh. Unknown argument: $*"
        usage
        exit 1
        ;;
    "exit" )
        exit 0
        ;;
    "regular" )
        script="$1"
        output="$2"
        shift 2
        if [[ $has_mockup == yes ]]; then
            MOCKUP=$(mktemp -d "_mockup.XXXXXX")
            _build/tezos-bin/tezos-client \
                --protocol $protocol \
                --base-dir $MOCKUP \
                create mockup
            $smartpyc "$script" --kind $kind --output "$output" --install $install_path --mockup $MOCKUP "$@" \
                && rm -rf $MOCKUP
        elif [[ $has_sandbox == yes ]]; then
            scripts/with_sandbox.sh sh -c \
            "$smartpyc $script --kind $kind --output $output --install $install_path $@"
        else
            $smartpyc "$script" --kind $kind --output "$output" --install $install_path "$@"
        fi
        ;;
    * )
        echo "Impossible action"
        exit 1
esac
