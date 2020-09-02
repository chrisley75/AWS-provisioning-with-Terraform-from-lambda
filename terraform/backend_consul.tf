terraform {
  backend "consul" {
    address = "consul.chrisley.fr:8500"
    path    = "tf/lambda"
  }
}
