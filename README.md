
# GitRanger

GitRanger is an API which will provide status of the open pull requests in your GitHub repository. 

  - Retrieve status of open PRs
  - Retrieve the list of open PRs
  - Retrieve the list of repositories

Note: **Currently only first 20 open PRs of the first 50 repositories will be retrieved.**

# Example

```
{
    "docker-workshop": {
        "prs": [
            {
                "id": 1,
                "state": "STATUS_CHECK_PENDING"
            }
        ]
    }
}
```
The above example displays that the repository "docker-workshop" has an open PR with id=1 and state=**STATUS_CHECK_PENDING**

## Sample API requests/API Documentation

Sample API requests and responses can be found here:
https://documenter.getpostman.com/view/3111950/RzfdpVfN
The API will be exposed as NodePort.

## Status List

 - If base branch is protected (https://help.github.com/articles/about-protected-branches/):
     - REVIEWER_PENDING (PR created, reviewer is not assigned and Require pull request reviews before merging protection added)
     - REVIEW_IN_PROGRESS (Reviewer is assigned, PR is not yet approved and equire pull request reviews before merging protection added)
     - STATUS_CHECK_PENDING (PR is approved, status checks are not reported and Require status checks to pass before merging protection added)
     - STATUS_CHECK_PENDING (status checks are not reported and Require status checks to pass before merging protection added)
     - FAILING (Status checks are failing for the PR and Require status checks to pass before merging protection added)
     - FAILING (PR is approved, Status checks are failing and Require pull request reviews before merging protection added)
     - MERGE_PENDING (PR is approved and status checks have passed)
 - If base branch is not protected: 
   In this case reviews **will not** be considered and only the status checks will be considered.
     - STATUS_CHECK_PENDING (Status checks are not reported)
     - FAILING (Status checks are failing)
     - MERGE_PENDING (Status checks have passed)

### Tech

GitRanger uses the following set of tools and technologies. Please take the following into consideration when deploying the Helm charts:

* Django (2.1.3) - To handle the API requests.
* PyGithub (1.43.3) - Library to access github repository data.
* PostgreSQL (10.6.0) - As database backend to the API.
* Nginx (1.15) - Proxy to the API.
* Helm (2.8.2) - To create kubernetes charts.
* Kubernetes (1.10.3) - To deploy GitRanger components 
* Docker Engine (18.09) - Container Engine for GitRanger components
* OS - Installer script has been tested on Mac (Mojave) and Centos (7.5)
* Postman - For API calls and documentation.
* Mozilla Firefox - Browser based API activities.

## Architecture
The GitRanger has the following basic architecture:
![Architecture](https://raw.githubusercontent.com/aratik711/django/master/Screenshot%202018-11-30%20at%203.54.57%20PM.png)

* The Nginx (port 80) acts as proxy service 
* Django (port 8000) provides API 
* Postgresql (port 5432) master serves read/write requests and slaves are read-only 
* Currently only one postgresql master is deployed per installation.


## Pre-requisites
* Kubernetes cluster (>=1.10.3) with kubectl.
* Docker (>=18.09)
* Helm (>=2.8.2)
* Tiller with RBAC permissions as mentioned here (https://docs.helm.sh/using_helm/#special-note-for-rbac-users)
* Envsubst
* OS Mac or Linux(Redhat/Debian - latest).
* Docker hub registry should be accessible.
* The API accepts GitHub access tokens, make sure that the token has the following permissions:
   * Access commit status
   * Access deployment status
   * Access public repositories
   In case you want GitRanger to access private repositories please give your accesstoken permissions accordingly.

## Installation

Install the pre-requisites and execute the following steps:
1. Untar the gitranger.tar.gz
``` tar -zxvf gitranger.tar.gz ```
2. Commands to create docker images (Optional, you can use the exisiting pre-built images at docker hub aratik711/). Docker images have already been created and pushed to hub.docker.com under the repository aratik711. If you want to rebuild the images use the following commands. Please change the repository name, image name and tag according to your choice. Do push your images to the docker hub registry.:
Note: Dockerfile.django uses a pre-built python image aratik711/python:3.6. Make sure that this image is accessible from your server. 

```
cd gitranger/
docker build -t aratik711/django:2.1 -f docker-images/Dockerfile.django ./docker-images
docker push aratik711/django:2.1  
docker build -t aratik711/nginx:1.15 -f docker-images/Dockerfile.nginx ./docker-images
docker push aratik711/nginx:1.15  
```
3. Edit the variables in install.sh, under section "Variables to be edited". (Default variables have been already added. you can skip this step if you haven't built images in previous step)
``` vi install.sh ```
    - postgresqlReplication - true/false - To enable/disable replication.
    - postgresqlUsername - (string) - username for postgresql.
    - postgresqlPassword - (string) - password for postgresql.
    - postgresqlDatabase - (string) - database for postgresql
    - apiExternalPort - (30000-32767) - This port will be used to connect to the GitRanger API.
    - apiUser - (string) - The username which will be used to login to the API.
    - apiPassword - (string) - The password which will be used to login to the API.
    - apiEmail - (email) - The email address of the above mentioned user.
    - djangoImageName - The image name of django image built in step 1. (Default: aratik711/django)
    - djangoImageTag - The image tag of django image built in step 1. (Default: 2.1)
    - nginxImageName - The image name of nginx image built in step 1. (Default: aratik711/nginx)
    - nginxImageTag - The image tag of nginx image built in step 1. (Default: 1.15)
Save the file.
4. Executable permission to script:
    ``` chmod +x install.sh ```
5. To install the GitRanger application execute the following command:
    ``` sh install.sh install ```
It will take a few minutes to deploy. Once the deployment is complete you will see a message as following:
GitRanger API is available at http://<IP>:<port> in the browser
6. Refer to the API documentation (https://documenter.getpostman.com/view/3111950/RzfdpVfN) for API usage instructions.

## Scale
Scaling the replicas for db, api and proxy tier is to be done manually. Do keep track of available resources before scaling up. Follow the below mentioned steps to scale
1. To scale db tier,
    ``` sh install.sh scale db <number-of-desired-replicas>```
    Example: ``` sh install.sh scale db 3```
This will scale postgresql slave replicas to 3. Currently scaling of only postgresql-slaves is permitted (If postgresqlReplication was set to true during installation)
2. To scale api tier
    ``` sh install.sh scale api <number-of-desired-replicas> ```
3. To scale proxy tier
    ``` sh install.sh scale proxy <number-of-desired-replicas> ```
You can scale up and scale down. Number of desired replicas should be >= 1.

## Cleanup
To cleanup/delete the GitRanger API deployment, Execute the following:
    ``` sh install.sh cleanup ```
    It will ask for confirmation press **y**
    In a few minutes the entire deployment will be deleted.
    
### Limitations
1. Only 1 PostgreSQL master because status/configuration of PV and volumes is unknown at clients end.
2. No ingress because status/installation of ingress controller is unknown at clients end.
3. Only 20 repositories and first 20 PRs each retrieved because performance and load testing is not yet done.
4. Have not yet tested HPA, so manual scaling is to be done.
5. Use Mozilla Firefox (preferably latest) when using the API in browser.
6. No LoadBalancer used because status of cloud dependency was unknown.
7. HTTP based requests, SSL certificates not added yet.
8. Currently tested with only public repositories.

### Known issues/Bugs:
1. If you receive this error in your response "tuple index out of range" or "ReadTimeout" please check your network and try again later. 

## Documentation
Please refer to the following document for API:
https://documenter.getpostman.com/view/3111950/RzfdpVfN

### Directory Structure

* ./django  =====> Django Helm chart
* ./postgresql ===> Postgresql Helm chart
* ./files   ===> All values files
* ./docker-images ===> Dockerfiles and dependent files
* ./nginx  ===> Nginx Helm chart

### Some other useful information

For administrative tasks related to API please use ``` <IP>:<Port>/admin/ ``` <br\>
Login with the credentials provided at the end of GitRanger installation.<br\>
You can add/update/delete new users with it.<br\>
Refer here for more details: https://djangobook.com/django-admin-site/

### Suggestions/Improvements
Drop me an email at ```aratik711@gmail.com```
