# Documentation of an automated deployment of simple API

This directory contains all the files needed in order to deploy the simple API on CentOS 7.x. The specific version that was tested is:

	- CentOS/RHEL 7.8

**Note**: Everything should work with any other major version of CentOS

## Requirements
In order for the playbooks to function properly, the following components should be installed on the system that is going to run the playbooks:

	- EPEL Repository if you are running CentOS Linux on your workstation
	- Ansible 2.9.9
	- Vagrant 2.2.9

For **CentOS** you would need to run the following commands **as root** or as user that has root priviledges:

	- yum install -y epel-release
	- yum install -y ansible

For **MacOS** you would need to run the following commands, assuming that you have brew package manager installed:

	- brew install ansible
	- Installing Vagrant:
	[Vagrant installation](https://learn.hashicorp.com/vagrant/getting-started/install)
	  

**Note**: For Vagrant to run you would need a provider. The code was tested with VirtualBox as Vagrant provider

## Usage
The structure of the directory which contains the code is shown below :

```
.
├── README.md
├── Vagrantfile
├── ansible.cfg
├── cloud.yml
├── inventory
└── roles
    ├── aws_setup
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       ├── aws_config.j2
    │       └── aws_creds.j2
    ├── cron_setup
    │   ├── defaults
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── pull_and_sync.sh.j2
    ├── deploy_app
    │   ├── defaults
    │   │   └── main.yml
    │   ├── files
    │   │   └── app
    │   │       ├── Dockerfile
    │   │       ├── configuration.ini
    │   │       ├── extract_data.py
    │   │       ├── http.conf
    │   │       └── requirements.txt
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── docker-compose.yml.j2
    ├── docker_setup
    │   ├── defaults
    │   │   └── main.yml
    │   ├── handlers
    │   │   └── main.yml
    │   └── tasks
    │       ├── CentOS.yml
    │       ├── docker-compose.yml
    │       └── main.yml
    └── preflight
        ├── defaults
        │   └── main.yml
        ├── tasks
        │   └── main.yml
        └── vars
            └── CentOS.yml

```
## Deploying the API
### Vagrant
The Ansible playbooks can be run either by spinning up a machine on AWS and putting the appropriate parameters on the ``` inventory ``` file (Public IP Address, SSH user and the path to the private key) or by using Vagrant running the following command:

1. ``` vagrant up ``` (Wait until the CentOS box is downloaded and the machine is up)

2. ``` vagrant ssh-config ``` From the output, get the path that is related to the  ``` IdentityFile ``` and put it as the value of the ``` ansible_ssh_private_key_file ``` under the inventory file

3. ``` ansible-playbook -i inventory cloud.yml --ask-vault-pass ```

4. Put the password of the vault and let the playbook run. After is finished, just point your Browser to:
``` http://192.168.50.11/countries?country=Czechia ```

### AWS EC2
If you choose to go with an EC2 instance, you would need to just replace the values under the inventory file with the information related to your EC2 instance and run **steps 3 and 4** only.

## Future improvements / Productionisation
### What is done

For the purposes of this PoC I have used the following repository for getting data:

``` https://github.com/CSSEGISandData/COVID-19/ ```

This repository contains different kind of files, so I filtered them and searched for data only on the CSV files. I have used an S3 bucket on my personal AWS account for storing the data. After cloning the repository on the machine, I sync it with the contents of the S3 bucket. I have created a cronjob that runs every day on the machine for this purpose. For storing AWS credentials for accessing the S3 bucket, I have used Ansible Vault. 

For the deployment of the simple API, I have used Docker Compose. The API is deployed along with Nginx which acts as Reverse proxy.

### Future considerations
For this API to be considered as production, the following things needs to be considered:

1. In a production system you don't use AWS credentials but you rather create a role which you attach directly to the instance that you want to have access to S3
2. For accessing S3 bucket from within the instance, you should use S3 endpoint so traffic remains inside your VPC, without going trough the Internet
3. Tests for Ansible roles should be written (e.g Molecule)
4. Tests for the API should be written (e.g unit tests)
5. Deploy the API as a specific user and not as root
6. Use HTTPS instead of HTTP
7. USE ALB instead of Nginx, in order to leverage the elasticity and high availability that Cloud provides
8. Use Swagger for building the API
