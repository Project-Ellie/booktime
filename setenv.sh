#!/bin/bash

if [[ $1 = 'test' ]]
then
  echo
  echo settings for unit tests
  export DJANGO_SETTINGS_MODULE=booktime.settings.tests
  export DATABASE_HOST=localhost
  ok=y
elif [[ $1 = 'int' ]]
then
  echo
  echo settings for integration tests
  export DJANGO_SETTINGS_MODULE=booktime.settings.int_tests
  export DATABASE_HOST=localhost
  export DATABASE_USER=postgres
  export DATABASE_PASSWORD=postgres
  ok=y
elif [[ $1 = 'e2e' ]]
then
  echo
  echo settings for end-to-end tests
  export DJANGO_SETTINGS_MODULE=booktime.settings.e2e_tests
  ok=y
elif [[ $1 = 'info' ]]
then
  ok=y
else
  echo
  echo "usage: . ./setenv.sh [test|int|e2e]"
  echo "test: unit tests against sqllite3"
  echo "int:  integration tests against postgres"
  echo "e2e:  end-to-end tests with docker containers"
  echo
  ok=n
fi

if [[ $ok = 'y' ]]
then
  echo
  echo "DJANGO_SETTINGS_MODULE is set to: $DJANGO_SETTINGS_MODULE"
  echo "DATABASE_HOST is set to:          $DATABASE_HOST"
  echo
fi