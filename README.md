# Building-Hacking-Tools-From-Scratch

## [Presentation Poster Link](https://www.canva.com/design/DAGU2-71zNA/bffINJa6wHMd0bibsoQkyQ/edit?utm_content=DAGU2-71zNA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Set up Instructions

### Step 1: Target Machine
There are two options for setting up the target machine (locally or on AWS [Amazon Web Services])

#### Local hosting option
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

#### AWS Option
1. [Create/ Sign-in to your AWS account.](https://aws.amazon.com/ec2/)
2. Create an EC2 Instance
    2.1. Select "EC2" on the AWS dashboard. 
    ![AWS Instructions 1](./Instruction%20Images/AWS%20Instructions%201.png)
    2.2. Selecte "Launch an instance". 
    ![AWS Instructions 2](./Instruction%20Images/AWS%20Instructions%202.png)
    2.3. Name your instance and select "Ubuntu" for the OS Image.
    ![AWS Instructions 3](./Instruction%20Images/AWS%20Instructions%203.png)
    2.4. For "Key pair", select "Proceed without a key pair". For Network settings, tick the boxes for HTTP and HTTPS traffic. 
    ![AWS Instructions 4](./Instruction%20Images/AWS%20Instructions%204.png)
    2.5. Launch instance. 
    ![AWS Instructions 5](./Instruction%20Images/AWS%20Instructions%205.png)
3. Edit Security Group 
    3.1. Select "Security Groups" on the AWS dashboard. 
    ![AWS Instructions 6](./Instruction%20Images/AWS%20Instructions%206.png)
    3.2. Choose the new security group created (the name may be different from picture).
    ![AWS Instructions 7](./Instruction%20Images/AWS%20Instructions%207.png)
    3.3. Add new inbound rules so that new TCP protocol ports as shown in picture are accepted:.
    ![AWS Instructions 8](./Instruction%20Images/AWS%20Instructions%208.png)
4. Attach an elastic IP (so that the server's IP stays static). 
    4.1. Select "Elastic IPs" on the AWS dashboard.
    ![AWS Instructions 9](./Instruction%20Images/AWS%20Instructions%209.png)
    4.2. Select "Allocate Elastic IP Address". 
    ![AWS Instructions 10](./Instruction%20Images/AWS%20Instructions%2010.png)
    4.3. Choose "Allocate" to finish allocation. 
    ![AWS Instructions 11](./Instruction%20Images/AWS%20Instructions%2011.png)
    4.4. Select the newly allocated IP address. Within "Actions" choose "Associate Elastic IP address". 
    ![AWS Instructions 12](./Instruction%20Images/AWS%20Instructions%2012.png)
    4.5. Choose the recently created EC2 instance. 
    For private IP address, select whichever IP address is provided. 
    Click "Associate" and your instance now has a static IP address!
    ![AWS Instructions 13](./Instruction%20Images/AWS%20Instructions%2013.png)



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