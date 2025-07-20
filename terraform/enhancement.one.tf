# Russ Savela, russell.savela@snhu.edu, 2025


resource "aws_iam_role" "snhu_dynamodb" {
  name = "enhancement_one_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "enhancement_one_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  role = aws_iam_role.snhu_dynamodb

}


resource "aws_iam_instance_profile" "dynamodb_access" {
  name = "dynamodb-instance-profile"
  role = aws_iam_role.snhu_dynamodb
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
