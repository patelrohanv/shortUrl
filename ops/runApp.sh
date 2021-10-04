source ops/shortUrl.env

docker run --rm -d \
 --name postgres \
 -e POSTGRES_USER=$POSTGRES_USER \
 -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
 -e POSTGRES_DB=$POSTGRES_DB \
 -e POSTGRES_PORT=$POSTGRES_PORT \
 -p $POSTGRES_PORT:$POSTGRES_PORT \
 postgres

docker build -t shorturl-web -f ops\Dockerfile.flask .

docker run --rm -d \
 --name shorturl-web \
 -e FLASK_HOST=$FLASK_HOST \
 -e FLASK_PORT=$FLASK_PORT \
 -e FLASK_APP=$FLASK_APP \
 -e FLASK_ENV=$FLASK_ENV \
 -e POSTGRES_USER=$POSTGRES_USER \
 -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
 -e POSTGRES_DB=$POSTGRES_DB \
 -e POSTGRES_HOST=$POSTGRES_HOST \
 -e POSTGRES_PORT=$POSTGRES_PORT \
 -p $FLASK_PORT:$FLASK_PORT \
 shorturl-web