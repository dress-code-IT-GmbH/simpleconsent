#!/bin/bash -e

main() {
    init
    if [[ -e "$APPHOME/simpleconsent/database_is_initialized" ]]; then
        echo 'database already initialized'
        exit 0
    else
        touch $APPHOME/simpleconsent/database_is_initialized
    fi
    migrate
    createsuperuser
    load_auth_group_perms
}


init() {
    scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
    source $scriptsdir/setenv.sh
    APPHOME=$(dirname $scriptsdir)
}


migrate() {
    rc=$(python $APPHOME/manage.py migrate)
    if (( rc > 0 )); then
        echo "failed to create database schema, migrate returned with ${rc}"
        exit 1
    else
        echo 'Initial database migration complete'
    fi
}


createsuperuser() {
    rc=0
    [[ $DEFAULT_USER ]] || DEFAULT_USER="admin"
    [[ $DEFAULT_EMAIL ]] || DEFAULT_EMAIL="admin@local"
    [[ $DEFAULT_PASS ]] || DEFAULT_PASS="adminadmin"
    echo "from django.contrib.auth.models import User; "\
         "User.objects.create_superuser('$DEFAULT_USER', "\
         "'$DEFAULT_EMAIL', '$DEFAULT_PASS')" |\
         $APPHOME/manage.py shell || rc=$?
    if ((rc>0)); then
        echo "manage.py createsuperuser failed with ${rc}"
        exit 1
    else
        echo 'DB superuser created'
    fi
}

load_auth_group_perms() {
    python manage.py loaddata data/auth_permissions_init.json
    #python manage.py loaddata data/auth_groups_init.json
}


main $@
