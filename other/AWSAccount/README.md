
# AWS Account Setup and Configuration

Follow the steps below to set up and configure an AWS account and grant necessary permissions for the project.

## 1. Account Registration

- Visit [AWS Official Website](https://aws.amazon.com/) and register an account.

## 2. Access the IAM Service

- After registering, search for the IAM service or directly access it using [this link](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1).

![1](/image/aws/iam1.png)

## 3. Create a New User

- In the left pane, select **Users** and click **Create User**.
![](/image/aws/iam2.png)
![](/image/aws/iam3.png)
- Input your desired user name.
![](/image/aws/iam4.png)
- Choose **Attach policies directly**.
![](/image/aws/iam5.png)
## 4. Attach Policies

Attach the following policies to the user:
- `AmazonEC2FullAccess`
- `AmazonRDSFullAccess`
- `AmazonS3FullAccess`
- `AmazonVPCFullAccess`

![](/image/aws/iam6.png)

Ensure that your selection matches the policies listed above.

## 5. User Creation and Access

- Click **Create**.
- Access the user you just created.
![](/image/aws/iam7.png)
- Navigate to **Security credentials**.
- Under **Access keys**, click **Create access keys**.
![](/image/aws/iam8.png)

## 6. Create Access Key for Other Use Cases

- Select **Other use case**.
![](/image/aws/iam9.png)
- Input any description you find necessary.
- Click **Create access key**.
![](/image/aws/iam10.png)
## 7. Save the Access Key
![](/image/aws/iam11.png)

Make sure to save the created access key. You will need to input this key into the `.env` file later.
---
