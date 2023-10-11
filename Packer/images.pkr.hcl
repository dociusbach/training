packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1"
    }
  }
}
source "amazon-ebs" "docker-host" {
  #where to get the images
  #where to save the images
  profile           = "default"
  ami_name          = "docker-host-hoh"
  source_ami        = "ami-053b0d53c279acc90"
  instance_type     = "t2.micro"
  region            = "us-east-1"
  ssh_username      = "ubuntu"
  vpc_id            = "vpc-0e57a0c5fb35800ab"
  subnet_id         = "subnet-0592d470a11220f5e"
  security_group_id = "sg-0614e69dca9b35ed3"
  tags = {
    name         = "PACKER-DOCKER-IMAGE"
    organization = "HOH"
  }
}
build {
  #install
  #Configure
  #files
  sources = [
    "source.amazon-ebs.docker-host"
  ]
  provisioner "file" {
    source      = "./id_ed25519.pub"
    destination = "/tmp/id_ed25519.pub"
  }
  provisioner "shell" {
    script = "./setup.sh"
  }

}