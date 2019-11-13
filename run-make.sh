#!/usr/bin/env bash
#

if [ $# -lt 1 ]
then
	usage="This is a make wrapper that loads env variables from /etc/webapi/webapi.env, ~/.webapi.env, .webapi.env, \${WEBAPI_CONF_ENV_LAST_RESORT} before calling make. Last declared env variable value overrides previous values. Eg: run-make.sh run"
	echo $usage;
	exit -1
fi

pushd .
cd -P -- "$(dirname -- "$0")"


set -o allexport

if [ -f /etc/webapi/webapi.env ]
then
    source /etc/webapi/webapi.env
fi
if [ -f ~/.webapi.env ]
then
    source ~/.webapi.env
fi
if [ -f .webapi.env ]
then
    source .webapi.env
fi
if [ -f .env ]
then
    source .env
fi
if [ -f ${WEBAPI_CONF_ENV_LAST_RESORT:-""} ]
then
    source ${WEBAPI_CONF_ENV_LAST_RESORT}
fi


set +o allexport
make $@
popd
