#!/bin/bash

set -e

export POSTGRESQL_CHART_NAME=gitranger-db
export DJANGO_CHART_NAME=gitranger-api
export NAMESPACE=gitranger

##### VARIABLES TO BE EDITED #################

##PostgreSQL variables
export postgresqlReplication=true
export postgresqlUsername=gituser
export postgresqlPassword=zqinehcMF95usc2k
export postgresqlDatabase=gitranger

##Django variables
export apiExternalPort=30008


#############################################

############################################

## Function to install mysql, wordpress and varnish

install() {

if [ -z "$postgresqlReplication" ] || [ -z "$postgresqlUsername" ] || [ -z "$postgresqlPassword" ] || \
   [ -z "$postgresqlDatabase" ] || [ -z "$apiExternalPort" ]; then

  echo 'ERROR: one or more variables are undefined'
  exit 1

fi

kubectl create namespace $NAMESPACE

## Create PostgreSQL deployment

envsubst < files/postgresql-values.yaml > postgresql/values.yaml

helm install --name $POSTGRESQL_CHART_NAME --namespace $NAMESPACE postgresql

kubectl rollout status statefulsets ${POSTGRESQL_CHART_NAME}-postgresql-master --namespace $NAMESPACE
kubectl rollout status statefulsets ${POSTGRESQL_CHART_NAME}-postgresql-slave --namespace $NAMESPACE

## Create Django deployment

envsubst < files/django-values.yaml > django/values.yaml

helm install --name $DJANGO_CHART_NAME --namespace $NAMESPACE django

kubectl rollout status deployment ${DJANGO_CHART_NAME}-django --namespace $NAMESPACE

}

if ! command -v helm >/dev/null; then

  echo 'Please install helm first'
  exit 1

elif [ -z "$POSTGRESQL_CHART_NAME" ] || [ -z "$DJANGO_CHART_NAME" ]; then

  echo "Chart names undefined"
  exit 1

else

  "$@"

fi