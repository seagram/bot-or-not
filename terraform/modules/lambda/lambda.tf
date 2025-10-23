resource "aws_iam_role" "lambda" {
  name = "${var.app_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_ssm" {
  name = "${var.app_name}-lambda-ssm-policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ssm:GetParameter",
        "ssm:GetParameters"
      ]
      Resource = var.api_keys_parameter_arn
    }]
  })
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.app_name}"
  retention_in_days = 7
}

resource "null_resource" "lambda_build" {
  triggers = {
    requirements = filesha1("${path.module}/../../../pyproject.toml")
    src_hash     = sha1(join("", [for f in fileset("${path.module}/../../../src", "**") : filesha1("${path.module}/../../../src/${f}")]))
  }

  provisioner "local-exec" {
    command = <<-EOT
      cd ${path.module}/../../..
      rm -rf .lambda_package
      mkdir -p .lambda_package
      docker run --rm \
        -v "$(pwd):/workspace" \
        -w /workspace \
        public.ecr.aws/lambda/python:3.12 \
        bash -c "pip install --target .lambda_package --no-cache-dir -r pyproject.toml"
      cp -r src .lambda_package/
    EOT
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../.lambda_package"
  output_path = "${path.module}/lambda_function.zip"

  depends_on = [null_resource.lambda_build]
}

resource "aws_lambda_function" "app" {
  function_name = var.app_name
  role          = aws_iam_role.lambda.arn
  handler       = "src.lambda_handler.handler"
  runtime       = "python3.12"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  timeout     = 30
  memory_size = 512

  environment {
    variables = {
      TURSO_DATABASE_URL  = var.turso_database_url
      TURSO_AUTH_TOKEN    = var.turso_auth_token
      API_KEYS_PARAM_NAME = var.api_keys_parameter_name
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy_attachment.lambda_basic,
  ]
}

resource "aws_lambda_function_url" "app" {
  function_name      = aws_lambda_function.app.function_name
  authorization_type = "NONE"

  cors {
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["*"]
    expose_headers    = ["*"]
    max_age           = 86400
  }
}

