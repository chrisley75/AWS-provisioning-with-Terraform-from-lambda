output "EC2_HOSTNAME" {
  value = "${aws_instance.ec2.*.public_dns}"
}

output "EC2_PUB_ADDR" {
  value = "${aws_instance.ec2.*.public_ip}"
}
