source ./.production

mkdir -p ./build

SRC=./build/src

./po_compile.sh

cp -r ./addon ./reqs ./src ./manage.py ./build/

rm -rf ${SRC}/{fixtures,legacy,public,search/whoosh_index,local_settings.py,*sqlite}

mv ${SRC}/prod_settings.py ${SRC}/local_settings.py

find ./build -type f \
    -name '*.py' \
    -and ! -name 'wsgi.py' \
    -and ! -wholename '*/migrations/*.py' \
    -and ! -wholename '*/commands/*.py' \
    -exec py_compilefiles {} \; \
    -delete

find ${SRC} -type f -name '*.po' -delete

echo "Rsync project with ${USER}@${HOST}:${CODE_DIR}"
rsync --stats --archive --recursive --update ./build/* ${USER}@${HOST}:${CODE_DIR}/

rm -rf ./build
