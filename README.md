# TheKev.in

This is where my personal website lives. Check it out [here!](http://thekev.in)

## Deploy

Since you only really need the `docker-compose.yml` file for deployment, you
can deploy with:

    curl https://raw.githubusercontent.com/TheKevJames/thekev.in/master/docker-compose.yml > thekevin.yml
    docker stack deploy -c thekevin.yml thekevjames

You can update to the latest build with:

    docker service update --force thekevjames_thekevin

## Secrets

This project requires access to some secret keys; you can set these with:

    echo "my-dropbox-token" | docker secret create dropbox_token -
    echo "my-sentry-dsn" | docker secret create dentry_dsn_thekevin -
