Welcome to your new dbt project!

This dbt project runs inside a glue interactive session using databases that already exists.

#REQUIREMENTS
For cloud or local setup you must have

- IAM Role with glue-dbt role that should be placed on ./profiles/profiles.yml (Use this IAM Policy as reference and replace <> variables with your data [sample_iam_policy](../iam/glue_dbt_sample_policy.json))

## Local Setup
- Python 3 Installed (version 3.9 or higher).
- Dbt-core and dbt-glue installed.
- AWS CLI Installed and configured with an user that can create glue interactive sessions and also can use IAMPassRole.
```sh
pip install dbt-core dbt-glue
```
### Testing local Setup
```sh
dbt seed --profiles-dir ./profiles/ --vars '{source_glue_db: "<source_glue_db>", target_glue_db: "<source_glue_db>", target_s3_bucket: "<source_s3_uri>"}' --debug
dbt debug --profiles-dir ./profiles/ --vars '{source_glue_db: "<source_glue_db>", target_glue_db: "<source_glue_db>", target_s3_bucket: "<target_s3_uri>"}'
dbt run --profiles-dir ./profiles/ --vars '{source_glue_db: "<source_glue_db>", target_glue_db: "<target_glue_db>", target_s3_bucket: "<target_s3_uri>"}' --debug
```

## Cloud Setup
- Glue Job with pyshel command confgiured with dbt-core and dbt-glue created using the script [dbt_runner.py](../scripts/dbt_runner.py).
- The glue job must have permissions to create interactive sessions and iampassroles to pass the IAM role that is specified in profiles. Also it must have permissions to read and see buckets where the dbt projects are in.
- Upload the DBT Project inside a S3 Bucket.
- 

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
