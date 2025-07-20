# Russ Savela, russell.savela@snhu.edu, 2025


resource "aws_iam_instance_profile" "dynamodb_access" {
  name = "dynamodb-instance-profile"
  role = aws_iam_role.snhu_dynamo
}

resource "aws_instance" "enhancement-one" {


  ami                    = var.aws_ami
  instance_type          = "t4g.small"
  key_name               = var.aws_keyname
  monitoring             = true
  vpc_security_group_ids = var.aws_sgs
  subnet_id              = var.aws_subnet
  iam_instance_profile   = aws_iam_instance_profile.dynamodb_access

  user_data              = file("./user-data/config-deps.sh")

  tags = {
    Name        = "enhancement-one"
    Terraform   = "true"
    Environment = "dev"
  }
}
