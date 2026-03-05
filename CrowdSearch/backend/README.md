# Instructions for how to connect to the AWS development server

## Create EC2 Instance
1. Login to the AWS console and navigate to EC2
2. Navigate to instances and select launch instances
3. Name the instance something that you will remember
4. Leave the application section as is with the Amazon Linux selected
5. Make sure the t2.micro instance type is selected
6. Create a new RSA .pem key pair and save it somewhere secure
7. For network security create a security group and allow SSH traffic from anywhere
8. Now click launch instance to complete the setup

## Set Elastic IP Address
1. Navigate to EC2 elastic IPs under network & security
2. Select allocate elastic IP
3. Leave default settings and click allocate
4. Manually set the name to something unique
5. Select the IP address
6. Select actions and associate the elastic IP address
7. Choose the rds_proxy instance
8. Leave other defaults and select associate
9. Record the allocated elastic IP address

## Tunnel to RDS Server
1. Run chmod 400 \<Path to Key> in your terminal to set permissions
2. Run ssh -i \<Path to Key> -N -L 5432:crowd-search.craysg28gzdu.us-east-2.rds.amazonaws.com:5432 ec2-user@\<Elastic IP Address>

Leave the tunnel running and initiate the backend in a separate terminal.
