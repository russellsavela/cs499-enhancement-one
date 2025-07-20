# cs499-enhancement-one
Software Design and Engineering Submodule

This refactors the CS-340 Project Two code to be deployed via Terraform,
using Github Actions is as the CI/CD pipeline

## Usage

This code assumes that the github environment secrets AWS_ACCESS_KEY_ID
and AWS_SECRET_ACCESS_KEY have been set and have appropriate permissions
for the account being used. It also depends on these credentials being
set in the Terraform HCP Cloud.

Any commit to the main branch will trigger a deployement.

The artifact is now deployed via a commit to the main branch on Github, which triggers a Github Action defined in .github/workflows/deploy.yaml to execute a Terraform apply.   Terraform is configured to maintain the state of the infrastructure in HCP Cloud.  The deployment creates an AWS EC2 instance, which is bootstrapped from the terraform/user-data/config-deps.sh script.  This script installs dependencies on the instance and then runs the refactored application code.

TODO: [X] setup Terraform HCL state
      [ ] Complete CRUD layer chnages
