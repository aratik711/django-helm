#!/bin/bash

set -e

export POSTGRESQL_CHART_NAME=gitranger-db
export DJANGO_CHART_NAME=gitranger-api

##### VARIABLES TO BE EDITED #################

##PostgreSQL variables
export postgresqlReplication=true
export postgresqlUsername=gituser
export postgresqlPassword="zqinehcMF95usc2k"
export postgresqlDatabase=gitranger

##Django variables
export apiExternalPort=30008


