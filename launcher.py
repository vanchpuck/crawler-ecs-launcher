import boto3

# def lambda_handler(event,context):
CLIENT = boto3.client("ecs")


def register_task_definition():
    response = CLIENT.register_task_definition(
        family='gear-scanner-crawler',
        taskRoleArn='ecsTaskExecutionRole',
        executionRoleArn='ecsTaskExecutionRole',
        networkMode='awsvpc',
        containerDefinitions=[
            {
                "essential": True,
                "image": "848625190772.dkr.ecr.us-east-2.amazonaws.com/gear-scanner-crawler:latest",
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/gear-scanner-crawler",
                        "awslogs-region": "us-east-2",
                        "awslogs-stream-prefix": "gear-scanner-crawler"
                    }
                },
                "name": "gear-scanner-crawler"
            }
        ],
        requiresCompatibilities=[
            'FARGATE',
        ],
        cpu='1024',
        memory='2GB',
    )
    return str(response)


def run_task():
    response = CLIENT.run_task(
        cluster="GearScannerCrawlerCluster",
        launchType="FARGATE",
        taskDefinition="gear-scanner",
        count=1,
        platformVersion="LATEST",
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ["subnet-0c8f9fe0420462ca9", "subnet-0cb172e1bde8ca24e"],
                'assignPublicIp': "ENABLED",
                'securityGroups': ["sg-07e40bc566db457e4"]
            },
        }
    )
    return str(response)


def lambda_handler(event, context):
    return run_task()
