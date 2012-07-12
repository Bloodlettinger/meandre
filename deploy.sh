source ./.production

BUILD=./build
SRC=${BUILD}/src

mkdir -p ${BUILD}

./po_compile.sh

cp -r ./addon ./reqs ./src ./manage.py ./logs ${BUILD}

rm -rf ${SRC}/{fixtures,legacy,public,search/whoosh_index,local_settings.py,*sqlite}
rm -rf ${BUILD}/logs/*

mv ${SRC}/prod_settings.py ${SRC}/local_settings.py

find ${BUILD} -type f \
    -name '*.py' \
    -and ! -name 'wsgi.py' \
    -and ! -wholename '*/migrations/*.py' \
    -and ! -wholename '*/commands/*.py' \
    -exec py_compilefiles {} \; \
    -delete

find ${SRC} -type f -name '*.po' -delete

echo "Rsync project with ${USER}@${HOST}:${CODE_DIR}"
rsync --stats --archive --recursive --update ${BUILD}/* ${USER}@${HOST}:${CODE_DIR}/

rm -rf ${BUILD}
