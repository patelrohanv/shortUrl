 source ops/shortUrl.env
 docker run \
  --rm -d \
  --name postgres \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  -p $POSTGRES_PORT:$POSTGRES_PORT \
  postgres