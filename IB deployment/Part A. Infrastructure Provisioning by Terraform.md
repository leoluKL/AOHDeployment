# 1 Preparation
## 1.1 Prepare Installation Environment
- __Installation Computers__
    
    `NOTE: ST Engineering OA laptop is not suitable for the platform deployment. The deployment practise needs installing several software tools, such as AWS Cli, that OA laptop prohibit installing these tools.`

    A computer with a internet browser is needed to deploy AOH platform. Below software are essential tools:
    
    - AWS CLI
    - VS Code
    - Kubectl
    - Helm
    - Git

    If the OS of this computer is windows OS, it is recommended to provision a linux VM with the above tools installed, except VS Code. Because some scripts may not be correctly executed in windows environment.   

- __Terraform scripts__

    The terraform scripts are located in folder ar2-infra/terraform/terraform-aws-eks-blueprints-v4/deployment/. There is a sample subfolder "wfm-qa" that contains the IaC scripts. This folder name will be used as the AWS EKS service name. That means if the sample folder "wfm-qa" is used, the deployment cluster name will be "wfm-qa". There are other resources and configuration in the scripts will be also based upon name "wfm-qa".

    To create a deployment environment with another base name, you need to duplicate "wfm-qa" folder and replace the base string "wfm-qa" with your preferred cluster name. This basename replacement operation needs to be applied not only in ar2-infra folder, but also in a few other folders such as ar2-web-infra. Since this starting chapter only talks about infrastructure service provisioning, we will leave the explaination of other changes for adopting a customized cluster name in chapter 2.

    The below script shows how to generate a new IaC scripts folder to deploy AOH platform of customized cluster name "new-cluster-name". 
    
    `NOTE: Do not use upper case character in the cluster name string.`
    ```bash
    mkdir ./ar2-infra/argocd/new-cluster-name/
    cp -R ar2-infra/argocd/wfm-qa/* ar2-infra/argocd/new-cluster-name

    mv ar2-infra/argocd/new-cluster-name/root-app-wfm-qa.yml ar2-infra/argocd/new-cluster-name/root-app-new-cluster-name.yml

    mv ar2-infra/argocd/new-cluster-name/projects/project-wfm-qa.yml ar2-infra/argocd/new-cluster-name/projects/project-new-cluster-name.yml

    cd ar2-infra/argocd/new-cluster-name

    find . -type f -exec sed  -i "s/wfm-qa/new-cluster-name/g"  {} +
    ```



## 1.2 IaC Script Explaination
# 2 Provision Infrastructure in AWS

# 3 Post Setup
[set kubectl integration]
[Scale up/down cluster to save cost]


