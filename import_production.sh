source ./.production

rsync --verbose --archive --delete ${USER}@${HOST}:site1/src/public/media ./src/public/
rsync --verbose --archive --delete ${USER}@${HOST}:site1/dump.sql ./tmp/

python manage.py dbshell << EOF
\. ./tmp/dump.sql
EOF

rm -f ./tmp/dump.sql

exit 0
