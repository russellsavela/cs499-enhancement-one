
# Russ Savela, russell.savela@snhu.edu, 2025

terraform {

  cloud { 
    
    organization = "russell-savela-org" 

    workspaces { 
      name = "enhancement-one" 
    } 
  } 
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.67"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = var.aws_region
}

