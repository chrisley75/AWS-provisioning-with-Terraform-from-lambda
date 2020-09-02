
provider "aws" {
  region = "eu-west-3"
}


# amazon ami image
data "aws_ami" "Amazon_Linux_2_AMI" {
  most_recent   = true
  owners = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-2.0.????????-x86_64-gp2"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  filter {
      name   = "architecture"
      values = ["x86_64"]
  }
}

## Use case I use my own packer image
#data "aws_ami" "ec2-ami" {
#  filter {
#    name   = "state"
#    values = ["available"]
#  }
#  filter {
#    name   = "tag:BuiltBy"
#    values = ["Packer"]
#  }
#  most_recent = true
#  owners = ["self"]
#}

resource "aws_instance" "ec2" {
  ami		= data.aws_ami.Amazon_Linux_2_AMI.id
#  ami           = data.aws_ami.ec2-ami.id
  count		= var.number_vm
  instance_type = var.instance_type
  key_name = var.key_pair
  subnet_id = var.subnet_id

  tags = {
    Name     = "${var.instance_name}-${count.index + 1}-${timestamp()}"
    Owner    = "chrisley"
    App      = "lambda"
    Project  = "demo"
    Resource = "ec2"
  }
}
