from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_iam as iam,
    aws_glue as glue,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
from constructs import Construct

class DbtGlueStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. S3 bucket for dbt project
        dbt_bucket = s3.Bucket(self, "DBT_BUCKET", bucket_name="vigia-data-lake-dl-artifacts-dbt-dev-a14b31")

        # 1.1 Upload runner to S3
        dbt_object_runner_script = s3_deploy.BucketDeployment(
            self, "DBT_RUNNER"
            , sources=[s3_deploy.Source.asset("./scripts/")]
            , destination_bucket=dbt_bucket,
        )
        
        # 1.2 Upload dbt project to S3
        dbt_object_runner_script = s3_deploy.BucketDeployment(
            self, "DBT_PROJECT"
            , sources=[s3_deploy.Source.asset("./poc_transformations_dbt/")]
            , destination_bucket=dbt_bucket,
        )
        
        
        # 2. IAM Role for Glue
        glue_role = iam.Role(
            self, "GlueRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com")
        )
        dbt_bucket.grant_read_write(glue_role)
        glue_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
        )

        # 3. Glue Job definition (dbt runner)
        glue_job = glue.CfnJob(
            self, "DbtGlueJob",
            role=glue_role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name="pythonshell",  # or "pythonshell"
                python_version="3",
                script_location=f"s3://{dbt_bucket}/scripts/dbt_runner.py"
            ),
            glue_version="4.0",
            default_arguments={
                "--additional-python-modules": "dbt-core,dbt-spark",  # packaged libs
                "--TempDir": f"s3://{dbt_bucket}/temp/"
            }
        )

        # 4. Step Functions workflow to orchestrate dbt commands
        start_glue = tasks.GlueStartJobRun(
            self, "RunDbt",
            glue_job_name=glue_job.ref,
            arguments=sfn.TaskInput.from_object({
                "--command": "dbt run --profiles-dir /tmp/profiles --project-dir /tmp/project"
            }),
            integration_pattern=sfn.IntegrationPattern.RUN_JOB
        )

        definition = start_glue

        sm = sfn.StateMachine(
            self, "DbtOrchestration",
            definition=definition
        )