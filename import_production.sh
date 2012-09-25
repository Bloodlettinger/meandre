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

ssh ${HOST_USER}@${HOST_NAME} "mysqldump -h ${DB_HOST} -u ${DB_USER} -p${DB_PASS} ${DB_NAME} > ~/site1/dump.sql"

rsync --verbose --archive --delete ${HOST_USER}@${HOST_NAME}:site1/src/public/media ./src/public/
rsync --verbose --archive --delete ${HOST_USER}@${HOST_NAME}:site1/dump.sql ./tmp/

python manage.py dbshell << EOF
\. ./tmp/dump.sql
EOF

exit 0
