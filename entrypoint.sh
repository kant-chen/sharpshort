#!/bin/bash
# set -ex
# for debugging env variables echo $(env)
#POSTGRES_DB=$(echo ${DATABASE_URL} | rev | cut -d '/' -f 1 | rev)
#echo $("echo $POSTGRES_DB")

_print_status() {
    # Show   red x if last command failed
    # Show green o if last command succeeded
    case $? in
        0) printf '\342\234\224\n' ;;
        *) printf '\342\234\227\n' ;;
    esac
    history -a
    true
}

function createdb {
    if psql -h $POSTGRES_HOST -U postgres -lqt | cut -d \| -f 1 | grep -qw ${POSTGRES_DB}; then
        echo "Database exists. Not creating"
    else
       psql -h $POSTGRES_HOST -U postgres -c "CREATE DATABASE ${POSTGRES_DB}"
       psql -h $POSTGRES_USER -U postgres -tc "SELECT 1 FROM pg_user WHERE usename = '${POSTGRES_USER}'" | grep -q 1 || psql -h "${POSTGRES_HOST}" -U postgres -c "CREATE ROLE ${POSTGRES_USER} LOGIN PASSWORD '${POSTGRES_PASWORD}'; ALTER USER ${POSTGRES_USER} CREATEDB;"
    fi
}

function migrate {
    echo $("pwd")
    python manage.py migrate
}


function assets {
    python manage.py collectstatic --noinput
}

function startdjango {
    python manage.py runserver 0.0.0.0:8000
}



function init {
    echo -n "Checking database"
    createdb
    _print_status
    echo -n "Migrating"
    migrate
    _print_status
    echo -n "Starting django"
    startdjango
    _print_status
}

function test {
    createdb
    migrate
    # all runnable tests are imported in central location under sharpshort.tests
    python manage.py test sharpshort.tests
}

eval $@
