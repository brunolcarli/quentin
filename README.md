<table align="center"><tr><td align="center" width="9999">

<img src="https://vectorportal.com/storage/tarantino-vector.jpg" align="center" width="170" alt="Project icon">

# Quentin

*Movie information discord bot*

</td></tr>

</table>    

<div align="center">

> [![Version badge](https://img.shields.io/badge/version-0.0.1-silver.svg)](https://lisa--brunolcarli.repl.co/graphql/?query=query%7B%0A%09lisa%0A%7D)


</div>

<hr /><br />

# Invite

To add the bot to your discord server use this [invitation](#addInviteLink).



# Development And Configuration


This section explains step-by-step the service configuration and running.

## Primary dependecies

To configure the service, first of all you should get two kinds of **tokens** from base platforms thaht powers the software:

- An API token from [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction);
- A bot token from [Discord Developers Portal](https://discord.com/developers/applications);


There are two basic ways to run this service:

- **Local machine*:
    + It is suggested for development;
- **Docker**:
    + It is suggested for production;
    + It is suggested when the environment or dependencies are not possible to configure on local machine;

## Run in local machine

### Local dependencies:

You smust have these dependencies installed on your machine:

- Python >= 3.8
- Redis-server
- Mysql-server


The service is a python based software, so you have to create a [python virtual environment](https://docs.python.org/3/tutorial/venv.html) to install the requirements, so, create and python venv, export a global environment variable to `development` and install the requirements from Makefile:

```
$ mkvirtualenv quentin
$ (quentin) export ENV_REF=development
$ (quentin) make install
```

Create a copy of the environment file template in `quentin/environment/export_template` and fill the values for the variables, such as the database user, host and passwords, the source the environment file you just created:

```
$ source quentin/environment/my_env_vars
```

Migrate the database:

```
$ make migrate
```

Finally run the service:

```
$ make run
```

## Run in Docker

### Local dependencies:

- Docker
- Python-pip

Install `docker-compose` from pip:

```
$ pip install docker-compose
```

Create an encironment file called `quentin_env` from the template in `quentin/environment/docker_template` and fill the blank variables, at the end you should have a filled env file in `quentin/environment/quentin_env`. Docker compose will look for the mentioned file in the mentioned directory. build and run the container:

```
$ docker-compose build && docker-compose up
```

## Testing

For testing you should follow the steps for running the service in your local machine, above described. In a virtual env, install the requirements and fill your env vars to set up database configurations, then run tests from makefile:


```
$ make test
```


## References

### - Quentin image:

Image by <a href=" https://www.vectorportal.com" >Vectorportal.com</a>,  <a class="external text" href="https://creativecommons.org/licenses/by/4.0/" >CC BY</a>; [Shmector](https://vectorportal.com/vector/director-quentin-tarantino/14537)

### - The Movie Database API


Powered by:

[API Backend](https://www.themoviedb.org/)

[![TMDB](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_long_1-8ba2ac31f354005783fab473602c34c3f4fd207150182061e425d366e4f34596.svg)](https://www.themoviedb.org/)
