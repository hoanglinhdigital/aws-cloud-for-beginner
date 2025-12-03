# Chuẩn bị
Cài đặt AWS CLI, cấu hình access key
Cài đặt Node, Typescript.
Cài đặt CDK
`npm install -g aws-cdk@2`
Kiểm tra bằng lệnh: `cdk --version`

# khởi tạo project CDK
Tạo mới thư mục tên: `my-ec2-cdk`
cd my-ec2-cdk
cdk init app --language typescript

#  Cấu trúc thư mục CDK:
my-ec2-cdk/
├── bin/
│   └── my-ec2-cdk.ts
├── lib/
│   └── my-ec2-cdk-stack.ts
├── package.json
├── cdk.json
└── tsconfig.json
...

# Copy đoạn code sau vào /lib/my-ec2-cdk-stack.ts
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class MyEc2CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Tạo VPC mặc định
    const vpc = new ec2.Vpc(this, 'MyVpc', {
      maxAzs: 2, // Sử dụng 2 Availability Zones
    });

    // Tạo EC2 instance
    const instance = new ec2.Instance(this, 'MyInstance', {
      vpc,
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T2,
        ec2.InstanceSize.MICRO
      ),
      machineImage: ec2.MachineImage.latestAmazonLinux2023(),
    });

    // Mở cổng SSH (port 22)
    instance.connections.allowFromAnyIpv4(ec2.Port.tcp(22), 'Allow SSH access');
  }
}

# Copy đoạn code sau vào /bin/my-ec2-cdk.ts
#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { MyEc2CdkStack } from '../lib/my-ec2-cdk-stack';

const app = new cdk.App();
new MyEc2CdkStack(app, 'MyEc2CdkStack');

# Triển khai lên AWS:
cdk bootstrap
cdk deploy

# Xóa resources
cdk destroy
