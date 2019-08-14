from aws_cdk import (
    aws_events,
    aws_iam,
    aws_lambda,
    aws_logs,
    aws_events_targets,
    core
)


class LambdaCronStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        jsonloggingLayer = aws_lambda.LayerVersion(self, 'jsonloggingLayer',
                                                   code=aws_lambda.AssetCode('layers/json_logging'),
                                                   compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_7],
                                                   layer_version_name="clean-lambda-versions-json_logging")

        pytzLayer = aws_lambda.LayerVersion(self, 'pytzLayer',
                                            code=aws_lambda.AssetCode('layers/pytz'),
                                            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_7],
                                            layer_version_name="clean-lambda-versions-ptyz")

        lambdaFn = aws_lambda.Function(
            self, "Singleton",
            code=aws_lambda.AssetCode('./src'),
            handler="handler.clean_lambda_versions",
            function_name="clean-lambda-versions",
            layers=[jsonloggingLayer, pytzLayer],
            log_retention=aws_logs.RetentionDays.ONE_YEAR,
            timeout=core.Duration.seconds(300),
            runtime=aws_lambda.Runtime.PYTHON_3_7,
        )
        lambdaFn.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=['lambda:ListFunctions',
                         'lambda:ListVersionsByFunction',
                         'lambda:DeleteFunction'],
                resources=['*'],
            )
        )

        # Run every monday at 08:01 AM UTC
        rule = aws_events.Rule(
            self, "Rule",
            schedule=aws_events.Schedule.cron(
                minute='01',
                hour='08',
                month='*',
                week_day='MON',
                year='*'),
        )
        rule.add_target(aws_events_targets.LambdaFunction(lambdaFn))


app = core.App()
LambdaCronStack(app, "clean-lambda-versions", env={'region': 'eu-west-1'})
app.synth()