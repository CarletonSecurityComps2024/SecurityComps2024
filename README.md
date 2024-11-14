# Building-Hacking-Tools-From-Scratch

## [Presentation Poster Link](https://www.canva.com/design/DAGU2-71zNA/bffINJa6wHMd0bibsoQkyQ/edit?utm_content=DAGU2-71zNA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## How to run Password Spraying Tool

### Step 1: Run Back End

```bash
cd TargetMachine/backend
npm install
node server.js
```

### Step 2: Run Front End

```bash
cd TargetMachine/frontend
npm install
npm run dev
```

### Step 3: Run Password Spraying

```bash
cd PasswordSprayingTool
python3 PasswordSprayingTool/password_spraying.py
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
