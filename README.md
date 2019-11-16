# Underwire

A toy gui program for sending encrypted messages over existing services.
Creates a secret channel to support your activities.

## Running

clone the repository

    pip install -r requirements.txt
    python underwire

## Setting up Gist Chat

To use the gist based encrypted chat you will need to obtain an oauth
token for your github account. Follow the instructions at the link.
This token will be entered in the login screen of the program to allow
the program to post and read messages from gists using your account.

https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line

### Joining a room (gist)

A gist id acts as the unique identifier for a 'chat room'. You may either
create a new gist and share that id to chat or join an existing room by
entering an existing gist id. By default gists are created as 'secret' and
are not indexed by search engines but they are public so be careful who you
share your gist id with.
