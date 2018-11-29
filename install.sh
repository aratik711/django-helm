#!/bin/bash

set -e

export POSTGRESQL_CHART_NAME=gitranger-db
export DJANGO_CHART_NAME=gitranger-api
export NGINX_CHART_NAME=gitranger-proxy
export NAMESPACE=gitranger

##### VARIABLES TO BE EDITED #################

##DB variables
export postgresqlReplication=true
export postgresqlUsername=gituser
export postgresqlPassword=zqinehcMF95usc2k
export postgresqlDatabase=gitranger

##API variables
export apiExternalPort=30080
export apiUser=git
export apiPassword=rGswMtQejL7g49e
export apiEmail=gitranger@example.com

##IMAGE variables
export djangoImageName=aratik711/django
export djangoImageTag=2.1
export nginxImageName=aratik711/nginx
export nginxImageTag=1.15

#############################################

############################################

## Function to install mysql, wordpress and varnish

install() {

if [ -z "$postgresqlReplication" ] || [ -z "$postgresqlUsername" ] || [ -z "$postgresqlPassword" ] || \
   [ -z "$postgresqlDatabase" ] || [ -z "$apiExternalPort" ] || [ -z "$apiUser" ] || \
   [ -z "$apiPassword" ] || [ -z "$apiEmail" ]; then

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

## Create Nginx deployment

envsubst < files/nginx-values.yaml > nginx/values.yaml

helm install --name $NGINX_CHART_NAME --namespace $NAMESPACE nginx

kubectl rollout status deployment ${NGINX_CHART_NAME}-nginx --namespace $NAMESPACE

GREEN='\033[0;32m'
NC='\033[0m' # No Color
printf "\n"
echo "${GREEN}GitRanger API is available at http://<IP>:$apiExternalPort in the browser.
Login with credentials $apiUser:$apiPassword ${NC}"
printf "\n"

}

## Delete all the deployments

cleanup() {

printf "\n"
read -p "Do you want to delete the deployments (y/n)? " yn
case $yn in
   [Yy]* ) helm delete --purge  ${POSTGRESQL_CHART_NAME} ${DJANGO_CHART_NAME} ${NGINX_CHART_NAME} || true
           kubectl delete namespace $NAMESPACE
           echo "The deployments have been deleted"
           break;;
   * ) exit;;
esac

}

## Function to scale GitRanger

scale() {

if [ -z $1 ]; then

  echo 'Please pass the name of the tier(db, api, proxy) to be scaled'
  exit 1

elif [ -z $2 ]; then

  echo "Please pass the desired number of replicas for $1 deployment"
  exit 1

elif [ $2 -ge 1 ]; then

  echo "Please pass the desired number of replicas for $1 deployment greater than or equal to 1"
  exit 1

else

  if [ "$1" = "db" ]; then
    DEPLOYMENT=${POSTGRESQL_CHART_NAME}-postgresql-slave
    RESOURCE=statefulset
  elif [ "$1" = "api" ]; then
    DEPLOYMENT=${DJANGO_CHART_NAME}-django
    RESOURCE=deployment
  elif [ "$1" = "proxy" ]; then
    DEPLOYMENT=${NGINX_CHART_NAME}-nginx
    RESOURCE=deployment
  else
    echo "No deployment $1 found. Deployments available (db, api, proxy)"
    exit 1
  fi

  kubectl scale ${RESOURCE} ${DEPLOYMENT} --replicas=$2

  kubectl rollout status ${RESOURCE} ${DEPLOYMENT}

fi

}


if ! command -v helm >/dev/null; then

  echo 'Please install helm'
  exit 1

elif ! command -v kubectl >/dev/null; then

  echo 'Please install kubectl'
  exit 1

elif ! command -v envsubst >/dev/null; then

  echo 'Please install envsubst'
  exit 1

elif [ -z "$POSTGRESQL_CHART_NAME" ] || [ -z "$DJANGO_CHART_NAME" ] || [ -z "$NGINX_CHART_NAME" ]; then

  echo "Chart names undefined"
  exit 1

else

  "$@"

fi