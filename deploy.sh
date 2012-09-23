BUILD=./build
SRC=${BUILD}/src

mkdir -p ${BUILD}

if [ "$#" == "0" ] || [ "$1" == "help" ]; then
    echo -en "\nUsage: `basename $0` <target> [<command> [<command> ...]]\n\n"
    echo -en "where <target> is:\n"
    echo -en "\t* production\n\t* testing\n\n"
    echo -en "where <command> is:\n"
    echo -en "\t* migrate\n"
    echo -en "\t* static\n"
    echo -en "\t* i18n\n"
    echo -en "\t* haystack\n"
    echo -en "\t* noapply\n"
    echo -en "\n"
    exit 0;
fi

./po_compile.sh

cp -r ./addon ./reqs ./src ./manage.py ./logs ${BUILD}

TARGET=$1
case ${TARGET} in
    production)
        echo -en "\n>>> TARGET: ${TARGET}\n\n"
        mv ${SRC}/prod1_settings.py ${SRC}/local_settings.py
        for i in $(\
            python src/settings_dump.py \
            PROD_HOST_NAME \
            PROD_HOST_USER \
            PROD_HOST_DIR \
            PROD_DB_HOST \
            PROD_DB_NAME \
            PROD_DB_USER \
            PROD_DB_PASS \
            ); do export $i; done;
        ;;
    testing)
        echo -en "\n>>> TARGET: ${TARGET}\n\n"
        mv ${SRC}/prod2_settings.py ${SRC}/local_settings.py
        for i in $(\
            python src/settings_dump.py \
            TEST_HOST_NAME \
            TEST_HOST_USER \
            TEST_HOST_DIR \
            TEST_DB_HOST \
            TEST_DB_NAME \
            TEST_DB_USER \
            TEST_DB_PASS \
            ); do export $i; done;
        ;;
    *)
        echo ">>> TARGET: UNKNOWN"
        exit 1
        ;;
esac

rm -rf ${SRC}/{fixtures,legacy,public,search/whoosh_index,prod[12]_settings.py,*sqlite}
rm -rf ${BUILD}/logs/*

echo -en "\nCompile project files\n\n"
find ${BUILD} -type f \
    -name '*.py' \
    -and ! -name 'wsgi.py' \
    -and ! -wholename '*/migrations/*.py' \
    -and ! -wholename '*/commands/*.py' \
    -exec py_compilefiles {} \; \
    -delete

find ${SRC} -type f -name '*.po' -delete

echo -en "\nRsync project with ${HOST_USER}@${HOST_NAME}:${HOST_DIR}\n\n"
rsync --stats --archive --recursive --update ${BUILD}/* ${HOST_USER}@${HOST_NAME}:${HOST_DIR}/

FAB="fab ${TARGET} deploy_server"
DELIM=":"
for param in $@; do
    if test 'migrate' = ${param}; then
        FAB="${FAB}${DELIM}migrate=True"
        DELIM=","
    fi
    if test 'static' = ${param}; then
        FAB="${FAB}${DELIM}static=True"
        DELIM=","
    fi
    if test 'i18n' = ${param}; then
        FAB="${FAB}${DELIM}i18n=True"
        DELIM=","
    fi
    if test 'haystack' = ${param}; then
        FAB="${FAB}${DELIM}haystack=True"
        DELIM=","
    fi
    if test 'noapply' = ${param}; then
        FAB="${FAB}${DELIM}touch=False"
        DELIM=","
    fi
done
${FAB}

rm -rf ${BUILD}
