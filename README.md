# cs499-enhancement-one
Software Design and Engineering Submodule

This refactors the CS-340 Project Two code to be deployed via Terraform,
using Github Actions is as the CI/CD pipeline

## Usage

This code assumes that the github environment secrets AWS_ACCESS_KEY_ID
and AWS_SECRET_ACCESS_KEY have been set and have appropriate permissions
for the account being used.

Any commit to the main branch will trigger a deployement.

TODO: setup Terraform HCL state
