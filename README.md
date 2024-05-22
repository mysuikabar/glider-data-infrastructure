# glider-data-infrastructure
A data infrastructure for analyzing glider flight log data.

## Architecture
![architecture](./figures/architecture.svg)

## dbt Docs
The dbt documentation, which includes the table schema, is hosted on GitHub Pages and can be accessed via the following link.

https://mysuikabar.github.io/glider-data-infrastructure/

## Deploy

#### Setting Up GCP Credentials
To run `dbt run` periodically from GitHub Actions, you need to register the following two variables as GitHub secrets:
- `GCP_PROJECT_ID`: The ID of your GCP project
- `GCP_CREDENTIALS`: The contents of the key file (in JSON format) associated with the service account that has BigQuery execution permissions

If you want to run `dbt run` locally, place the key file in the `secrets/` directory and set the `GCP_PROJECT_ID` as an environment variable.

#### Deploying Resources
Run the following command to ensure you have access to GCP.
```bash
gcloud auth application-default login
```

Navigate to the `infra/` directory.
Create a `terraform.tfvars` file based on the `terraform.tfvars.sample` file.
Then, run the following command to deploy the resources on GCP.
```bash
terraform apply
```