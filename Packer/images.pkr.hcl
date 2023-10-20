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
  profile           = "awsaml-079904783278-BAHSSO_Admin_Role"
  ami_name          = "CSN_ENV_HOH_GRAFANA_WEB_AMI"
  source_ami        = "ami-053b0d53c279acc90"
  instance_type     = "t2.medium"
  region            = "us-east-1"
  ssh_username      = "ubuntu"
  vpc_id            = "vpc-0a6ca6c0616e5d19c"
  subnet_id         = "subnet-01005b3af0799faf5"
  security_group_id = "sg-0644cff8deb2df12c"
  tags = {
    name         = "CSN_ENV_HOH_GRAFANA_WEB_AMI"
    organization = "HOH"
  }
}
build {

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