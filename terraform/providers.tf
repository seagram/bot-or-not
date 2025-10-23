terraform {
    backend "s3" {
        bucket="seagram-terraform-state-bucket"
        key="botornot/terraform.tfstate"
        region="us-east-1"
        use_lockfile = true
        encrypt      = true
    }
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "6.18.0"
        }
        null = {
            source  = "hashicorp/null"
            version = "~> 3.0"
        }
        archive = {
            source  = "hashicorp/archive"
            version = "~> 2.0"
        }
    }
}

provider "aws" {
    region = "us-east-1"
}