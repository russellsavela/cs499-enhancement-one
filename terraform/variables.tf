# Russ Savela, russell.savela@snhu.edu, 2025


variable "aws_region" {
    type = string
    default = "us-east-1"
    description = "AWS Region"
}

variable "aws_subnet" {
    type = string
    default = "subnet-639b7c49"
    description = "AWS Subnet"
}

variable "aws_sgs" {
    type = list
    default = ["sg-0f56567e2d18c7f69"]
    description = "AWS Security Groups"
}


variable "aws_keyname" {
    type = string
    default = "snhu"
    description = "AWS Key Name"
}

variable "aws_ami" {
    type = string
    default = "ami-0cd4eb0ae8debf650"
    description = "AWS AMI"
}
