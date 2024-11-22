# Building-Hacking-Tools-From-Scratch

## [Presentation Poster Link](https://www.canva.com/design/DAGU2-71zNA/bffINJa6wHMd0bibsoQkyQ/edit?utm_content=DAGU2-71zNA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Set up Instructions

### Step 1: Target Machine

There are two options for setting up the target machine (locally or on AWS [Amazon Web Services])

## Local hosting option

1. Clone the git repository into a folder:

```bash
git clone https://github.com/CarletonSecurityComps2024/SecurityComps2024.git
```

2. Install dependencies on the backend:

```bash
cd project/TargetMachine/backend
npm install
```

3. (Optional) Install dependencies on the frontend to see what the log-in page looks like:

```bash
cd project/TargetMachine/frontend
npm install
```

## AWS Option

1. [Create/ Sign-in to your AWS account.](https://aws.amazon.com/ec2/)
2. Create an EC2 Instance
   2.1. Select EC2 on the AWS Console.
   ![AWS Instructions 1](./Instruction%20Images/AWS%20Instructions%201.png)
   2.2. Selecte "Launch an instance".
   ![AWS Instructions 1](./Instruction%20Images/AWS%20Instructions%202.png)
   2.3. Name your instance and select "Ubuntu" for the OS Image.
   ![AWS Instructions 1](./Instruction%20Images/AWS%20Instructions%203.png)
   2.4. For "Key pair", select "Proceed without a key pair". For Network settings, tick the boxes for HTTP and HTTPS traffic.
   ![AWS Instructions 1](./Instruction%20Images/AWS%20Instructions%204.png)
   2.5. Launch instance.
   ![AWS Instructions 1](./Instruction%20Images/AWS%20Instructions%205.png)

### Step 2: Attacker Machine

1. Clone the git repository into a folder:

```bash
git clone https://github.com/CarletonSecurityComps2024/SecurityComps2024.git
```

2. Open the folder using VSCode.
3. Navigate to the spraying tool folder using the terminal:

```bash
cd project/PasswordSprayingtool/
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Instructions

1. On the target machine, run the following code to start the server:

```bash
cd project/TargetMachine/backend
npm start
```

2. On the attacker machine, run the following code to run the tool:

```bash
cd project/PasswordSprayingtool/
python3 password_spraying.py
```

## References

1. Oxylabs, Roberta Aukstikalnyte, "What is proxy rotation and why is it important?", https://oxylabs.io/blog/rotate-proxies-python
2. CrowdStrike, Bart Lenaerts-Bergmans, "Password Spraying", 2022, https://www.crowdstrike.com/en-us/cybersecurity-101/cyberattacks/password-spraying/,
3. Splunk, Shanika Wickramasinghe, 2023, "Password Spraying Attacks: What You Need To Know To Prevent Attacks", https://www.splunk.com/en_us/blog/learn/password-spraying.html
4. Semperis, Daniel Petri, 2024, "How to Defend Against a Password Spraying Attack, "https://www.semperis.com/blog/how-to-defend-against-password-spraying-attacks/
5. AWS, "Amazon EC2", https://aws.amazon.com/ec2/
6. AWS "Amazon EC2 Auto Scaling", https://aws.amazon.com/ec2/autoscaling/
7. NetApps, "EC2 Autoscaling: The Basics, Getting Started, and 4 Best Practices", https://spot.io/resources/aws-autoscaling/ec2-autoscaling-the-basics-and-4-best-practices/
8. Infura, "Python: How to perform batch requests with Infura", https://support.infura.io/building-with-infura/python/how-to-perform-batch-requests
