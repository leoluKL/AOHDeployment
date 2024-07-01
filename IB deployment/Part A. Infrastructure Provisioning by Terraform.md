__Table of Content__

&nbsp;&nbsp;&nbsp;&nbsp;[1 Preparation](#1-preparation)

&nbsp;&nbsp;&nbsp;&nbsp;[2 Provision Infrastructure in AWS](#2-provision-infrastructure-in-aws)

&nbsp;&nbsp;&nbsp;&nbsp;[3 Post Setup](#3-post-setup)


# 1 Preparation
## 1.1 Prepare Installation Environment
- __Installation Computers__
    
    `NOTE: ST Engineering OA laptop is not suitable for the platform deployment. The deployment needs installing several software tools, such as AWS Cli, while OA laptop prohibits installing these tools.`

    A computer with internet browser is needed to deploy AOH platform. Below software are essential tools to support the deployment.
    
    - AWS CLI
    - VS Code
    - Kubectl
    - Helm
    - Git

    If the OS of this computer is windows OS, it is recommended to provision another standby linux VM with the above tools installed, except VS Code, because some scripts can not correctly run in windows environment.   

- __Git Repositories__

    Several git repositories will be used in the deployment:
    - ar2-infra
    - demo-trip-infra
    - ar2-web-infra
    
    If you want to create customized cluster and different web application domain name, it is essential to copy them from the R&D team's repositories and create as your own GIT repositories. Essential modifation is going to be made in your own repositories.
    
    Another git repository in-use is aoh-db. Simply download it. You will use the script inside for database creation later.

    Note that both AOH deployment scripts for ArgoCD and IaC scripts for Terraform are inside the ar2-infra repository. 

    Before next step, download ar2-infra and aoh-db repositories to the installation computer.

- __Terraform scripts__

    The terraform scripts are in folder ar2-infra/terraform/terraform-aws-eks-blueprints-v4/deployment/. You shall see a sample subfolder "wfm-qa". 
    The scripts in this template folder will use "wfm-qa" as the AWS EKS service name. And many other infrastructure components and configuration of AOH platform will also contain "wfm-qa" base string.

    To create your own base string and cluster name for the deployment, you need to duplicate "wfm-qa" folder and search all files to replace the base string "wfm-qa" with your preferred string. You need to apply this string replacing in other repositories as well, such as ar2-web-infra. 
    
    Assume the new base string is "new-cluster-name", we need run below scripts: 
    
    `NOTE: Do not use upper case character in the cluster name string, otherwise the terraform script execution will fail.`
    ```bash
    # cd to the parent folder of ar2-infra
    
    mkdir ./ar2-infra/argocd/new-cluster-name/
    cp -R ar2-infra/argocd/wfm-qa/* ar2-infra/argocd/new-cluster-name

    mv ar2-infra/argocd/new-cluster-name/root-app-wfm-qa.yml ar2-infra/argocd/new-cluster-name/root-app-new-cluster-name.yml

    mv ar2-infra/argocd/new-cluster-name/projects/project-wfm-qa.yml ar2-infra/argocd/new-cluster-name/projects/project-new-cluster-name.yml

    cd ar2-infra/argocd/new-cluster-name

    find . -type f -exec sed  -i "s/wfm-qa/new-cluster-name/g"  {} +

    cd ../../..


    mkdir ./ar2-infra/terraform/terraform-aws-eks-blueprints-v4/deployment/new-cluster-name

    cp -R ar2-infra/terraform/terraform-aws-eks-blueprints-v4/deployment/wfm-qa/* ar2-infra/terraform/terraform-aws-eks-blueprints-v4/deployment/new-cluster-name

    cd ar2-infra/terraform/terraform-aws-eks-blueprints-v4/deployment/new-cluster-name

    find . -type f -exec sed  -i "s/wfm-qa/new-cluster-name/g"  {} +

    cd ../../../../..

    #-------------------------------

    mkdir ./ar2-web-infra/new-cluster-name/
    cp -R ar2-web-infra/wfm-qa/* ar2-web-infra/new-cluster-name

    cd ar2-web-infra/new-cluster-name
    find . -type f -exec sed  -i "s/wfm-qa/new-cluster-name/g"  {} +
    cd ../..

    #-------------------------------

    echo "It is done"

    ```


## 1.2 IaC Scripts Explaination
IaC scripts are in folder ar2-infra/terraform/terraform-aws-eks-blueprints-v4/deployment/new-cluster-name/. The main.tf file in this folder lists all the infrastructure components:
| No. | Terraform Components | Purpose |
| --- | --- | --- |
| 1 | module  "eks" | Provision EKS cluster, specify nodes group name and spec as well |
| 2 | module  "eks_blueprints_kubernetes_addons" | Install Kubernetes add-on |
| 3 | module "vpc" | Create VPC |
| 4 | resource "aws_kms_key"  "secrets" | Create an AWS KMS key. It will be used for encrypting and decrypt data (symmetric) |
| 5 | resource  "aws_secretsmanager_secret" "secret" | Create a secret in aws secret manager, it is also encrypted by using the key in item 4 |
| 6 | resource  "aws_secretsmanager_secret_version" "secret" | It sets the actual secret value for the above secret |
| 7 | resource "aws_iam_policy"  "cluster_secretstore" | Create a policy for grant access to item 4 and 5 |
| 8 | module  "cluster_secretstore_role" | create namespace and service accounts, the service account is with policy in item 7 |
| 9 | resource "kubectl_manifest"  "cluster_secretstore" | Create a clustersecretstore object in  K8s cluster. It will access secretes stored in AWS secrets manager. It uses the service account created by item 8 |
| 10 | resource "kubectl_manifest"  "secret" | Define an external secret in k8s cluster using cluster secret store item 9, the secret value is fetched from item 5 |
| ~~11~~ | ~~resource "aws_ssm_parameter" "secret_parameter"~~ | ~~Create a secret string is AWS systems parameter management~~ |
| ~~12~~ | ~~resource "aws_iam_policy"  "secretstore"~~ | ~~Create a policy to grant permissions to access all SSM parameters that are prefixed with your EKS cluster name within the specified region and AWS account~~  |
| ~~13~~ | ~~module "secretstore_role"~~ | ~~Create namespace and service accounts to use policy item 12~~ |
| ~~14~~ | ~~resource "kubectl_manifest"  "secretstore"~~ | ~~Create a secretstore in K8s cluster with role of item 13~~ |
| ~~15~~ | ~~resource "kubectl_manifest"  "secret_parameter"~~ | ~~Define an external secret in k8s cluster that fetch item 11~~ |

`NOTE: Item 11 to 15 are not used any more. This part will be removed from the IaC script in the future.`

# 2 Provision Infrastructure in AWS
Open a terminal in the installation computer and cd to your IaC scripts folder, for example, ar2-infra/terraform/terraform-aws-eks-blueprints-v4/deployment/new-cluster-name. Run below commands
```bash
# 3 Assume aws authentication is through sso login
aws configure
aws sso login

terraform init
terraform plan
terraform apply
```

# 3 Post Setup
- __Kubectl configuration__

    Setup local kubectl environment to access the AWS EKS cluster. Running
    ```bash
    # Assume the EKS resource is in region ap-southeast-1
    aws eks --region ap-southeast-1 update-kubeconfig --name new-cluster-name
    # test if it is configured correctly
    aws eks list-clusters
    ```

- __Scaling up/down EKS cluster__

    If the deployment is not for production environemnt, AWS service cost can be saved by turning off all EC2 worker nodes when the environment is not in use. Restore worker nodes only on demand. The cluster restoring time is about 10 minutes.

    ```bash
    # Scale down cluster to zero worker node to save cost
    aws eks update-nodegroup-config --cluster-name new-cluster-name \
    --nodegroup-name ${Actual node group name} \
    --scaling-config minSize=0,maxSize=1,desiredSize=0
    ```

    ```bash
    # Restore cluster worker nodes when in-use
    aws eks update-nodegroup-config --cluster-name new-cluster-name \
    --nodegroup-name ${Actual node group name, like initial_new-cluster-name-...} \
    --scaling-config minSize=2,maxSize=5,desiredSize=3
    ```


    
