# Russ Savela, russell.savela@snhu.edu, 2025


variable "aws_region" {
    type = string
    default = "us-east-1"
    description = "AWS Region"
}

variable "aws_subnet" {
    type = string
    default = ""
    description = "AWS Subnet"
}

variable "aws_sgs" {
    type = list
    default = [""]
    description = "AWS Security Groups"
}


variable "aws_keyname" {
    type = string
    default = "snhu"
    description = "AWS Key Name"
}
