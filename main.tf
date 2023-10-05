# Configure the AWS Provider
provider "aws" {
  region  = "us-east-1"
  profile = "default"
}

#Retrieve the list of AZs in the current AWS region
data "aws_availability_zones" "available" {}
data "aws_region" "current" {}
#Define the VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Name        = var.vpc_name
    Environment = "aws-test-lab"
    Terraform   = "true"
  }
}
resource "aws_subnet" "private_subnets" {
  for_each   = var.private_subnets
  vpc_id     = aws_vpc.vpc.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, each.value)
  availability_zone = tolist(data.aws_availability_zones.available.names)[
  each.value]
  tags = {
    Name      = each.key
    Terraform = "true"
  }
}
#Deploy the public subnets
resource "aws_subnet" "public_subnets" {
  for_each   = var.public_subnets
  vpc_id     = aws_vpc.vpc.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, each.value + 100)
  availability_zone = tolist(data.aws_availability_zones.available.
  names)[each.value]
  map_public_ip_on_launch = true
  tags = {
    Name      = each.key
    Terraform = "true"
  }
}
# Create route tables for public and private subnets
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
    #nat_gateway_id = aws_nat_gateway.nat_gateway.id
  }
  tags = {
    Name      = "aws_lab_public_rtb"
    Terraform = "true"
  }
}
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    #gateway_id = aws_internet_gateway.internet_gateway.id
    nat_gateway_id = aws_nat_gateway.nat_gateway.id
  }
  tags = {
    Name      = "aws_lab_private_route"
    Terraform = "true"
  }
}
#Create route table associations
resource "aws_route_table_association" "public" {
  depends_on     = [aws_subnet.public_subnets]
  route_table_id = aws_route_table.public_route_table.id
  for_each       = aws_subnet.public_subnets
  subnet_id      = each.value.id
}
resource "aws_route_table_association" "private" {
  depends_on     = [aws_subnet.private_subnets]
  route_table_id = aws_route_table.private_route_table.id
  for_each       = aws_subnet.private_subnets
  subnet_id      = each.value.id
}
#Create Internet Gateway
resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "aws_lab_igw"
  }
}
# #Create EIP for NAT Gateway
resource "aws_eip" "nat_gateway_eip" {
  domain     = "vpc"
  depends_on = [aws_internet_gateway.internet_gateway]
  tags = {
    Name = "aws_lab_igw_eip"
  }
}
#Create NAT Gateway
resource "aws_nat_gateway" "nat_gateway" {
  depends_on    = [aws_subnet.public_subnets]
  allocation_id = aws_eip.nat_gateway_eip.id
  subnet_id     = aws_subnet.public_subnets["public_subnet_1"].id
  tags = {
    Name = "aws_lab_gateway"
  }
}
# Terraform Data Block - To Lookup Latest Ubuntu 20.04 AMI Image
data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"]
}
resource "aws_security_group" "allow_ec2" {
  name        = "allow_tls"
  description = "Allow SSH"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_tls"
  }
}
# Terraform Resource Block - To Build EC2 instance in Public Subnet
resource "aws_instance" "web_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public_subnets["public_subnet_1"].id
  vpc_security_group_ids = [aws_security_group.allow_ec2.id]
  key_name = "bach"
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
  tags = {
    Name = "WEB-SERVER-AWS-LAB"
  }
}
resource "aws_iam_role" "EC2-ECR-Role"{
  name = "EC2-EKS-Role"
  assume_role_policy = jsonencode({
  
    "Version": "2012-10-17"
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
)
}
resource "aws_iam_role_policy_attachment" "EC2-ECR-Role-Mapping"{
  role = aws_iam_role.EC2-ECR-Role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
}
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.EC2-ECR-Role.name
}
# resource "aws_iam_policy" "EC2-EKS-Admin-Console-Access"{
#   name = "EC2-EKS-Admin-Console-Access"
#   policy = jsonencode({
#     "Version": "2012-10-17"
#     "Statement": [
#       {
#         "Sid": "VisualEditor0",
#         "Effect": "Allow",
#         "Action": "eks*",
#         "Resource": "*"
#       }
#     ]
#   })
# }

# resource "aws_iam_role" "EC2-EKS-Role"{
#   name = "EC2-EKS-Role"
#   assume_role_policy = <<POLICY
#   {
#     "Version": "2012-10-17"
#     "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "Service": "ec2.amazonaws.com"
#         },
#       "Action": "sts:AssumeRole"
#       } 

#     }
#     ]
#   }
#   POLICY
# description = "Allow EC2 Instances to Administer EKS Clusters"
# max_session_duration = "3600"
# }
# resource "aws_iam_role_policy_attachment" "EC2-EKS-Role-Mapping"{
#   role = aws_iam_role.EC2-EKS-Role
#   policy_arn = aws_iam_policy.EC2-EKS-Admin-Console-Access.arn
# }

# resource "aws_security_group" "eks-cluster-sg"{
#   name = "test-sg-eks-default"
#   vpc_id = aws_vpc.vpc.id
#   egress {
#     from_port = 0
#     to_port = 0
#     protocol = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   ingress{
#     from_port = 0
#     to_port = 0
#     protocol = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }
# resource "aws_eks_cluster" "eks-cluster" {
#   name = "test-eks-cluster"
#   role_arn = "${aws_iam_role.EC2-EKS-Role.arn}"
#   version = "1.27"
#   vpc_config {
#     security_group_ids = ["${aws_security_group.eks-cluster-sg.id}"]
#     subnet_ids = ["${aws_subnet.public_subnets["public_subnet_1"].id}"]
#   }
#   depends_on = [
#     "aws_iam_role_policy_attachment.EC2-EKS-Role-Mapping",
#    ]

# }
