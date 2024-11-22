# Multi-featured Approach to Crack HTTP Authentication

## [Poster Link](https://www.canva.com/design/DAGU2-71zNA/bffINJa6wHMd0bibsoQkyQ/edit?utm_content=DAGU2-71zNA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Set-up Instructions

### Step 1: Target Machine
There are two options for setting up the target machine (locally or on AWS [Amazon Web Services])

#### Local hosting option
1. Clone the git repository into a folder:
```bash
git clone https://github.com/CarletonSecurityComps2024/SecurityComps2024.git
```
2. Install dependencies on the backend:
```bash
cd SecurityComps2024/project/TargetMachine/backend
npm install
```

3. (Optional) Install dependencies on the frontend to see what the log-in page looks like:
```bash
cd SecurityComps2024/project/TargetMachine/frontend
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
5. Setting up dependencies on the EC2 instance.  
    5.1. Select "EC2" on the AWS dashboard.  
    5.2. Select the recently created EC2 instance and click on "Connect". 
    ![AWS Instructions 14](./Instruction%20Images/AWS%20Instructions%2014.png)
    5.3. Choose the "EC2 Instance Connect" option and click on "Connect". 
    ![AWS Instructions 15](./Instruction%20Images/AWS%20Instructions%2015.png)
    5.4. Install nginx, npm, and psql:  
    ```bash
    sudo apt-get update
    sudo apt install nginx -y
    sudo apt install npm -y
    sudo apt install postgresql -y
    ```  
    5.5. Setup postgres database.
    ```bash
    sudo -u postgres psql
    ```
    ```bash
    CREATE USER comps_user WITH PASSWORD 'comps_password';
    CREATE DATABASE comps;
    GRANT ALL PRIVILEGES ON DATABASE comps TO comps_user;
    ```
    5.6. Once the "comps" database is set up, set up the "blocked_ips" table.
    ```bash
    \c comps
    ```
    ```bash
    CREATE TABLE blocked_ips (
    id SERIAL PRIMARY KEY,
    ip_address INET NOT NULL,
    log_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE blocked_ips TO comps_user;
    ```
    5.7. Relocate to the target machine's backend folder.  
    ```bash
    cd SecurityComps2024/project/TargetMachine/backend/
    ```
    Create a ".env" file with the following:
    ```bash
    DB_USER=comps_user
    DB_HOST=localhost
    DB_DATABASE=comps
    DB_PASSWORD=comps_password
    DB_PORT=5432
    ```
6. Install dependencies.
    6.1. Install dependencies on the backend:
    ```bash
    cd SecurityComps2024/project/TargetMachine/backend
    npm install
    ```
    6.2. (Optional) Install dependencies on the frontend to see what the log-in page looks like:
    ```bash
    cd SecurityComps2024/project/TargetMachine/frontend
    npm install
    ```


### Step 2: Attacker Machine

1. Clone the git repository into a folder: 
```bash
git clone https://github.com/CarletonSecurityComps2024/SecurityComps2024.git
```
2. Open the folder using VSCode. 
3. Navigate to the spraying tool folder using the terminal: 
```bash
cd SecurityComps2024/project/PasswordSprayingtool/
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Add API credentials for proxy rotation. 
    5.1. Sign up for a free account on [Webshare.](https://www.webshare.io/home-page)
    ![Proxy API Instructions 1](./Instruction%20Images/Proxy1.jpg)
    5.2. After logging in, navigate to the Proxy List section in your dashboard.
    ![Proxy API Instructions 2](./Instruction%20Images/Proxy2.jpg)
    5.3. Click on the "Create API Key" button to generate a new key. You can assign a label to this key for easy identification.
    ![Proxy API Instructions 3](./Instruction%20Images/Proxy3.jpg)
    5.4. Go to Settings and retrieve API username and password.
    ![Proxy API Instructions 4](./Instruction%20Images/Proxy4.jpg)
    5.5. Relocate to the tool's folder.  
    ```bash
    cd SecurityComps2024/project/PasswordSprayingtool/
    ```
    Add the API credentials in this format:
    ```bash
    APIFY_PROXY_HOSTNAME=proxy.apify.com
    APIFY_PROXY_PORT=8000
    APIFY_PROXY_PASSWORD=***add_password_here***
    PROXY_API_KEY = ***add_api_key_here***
    PROXY_API_USERNAME = ***add_api_username_here***
    PROXY_API_PASSWORD = ***add_api_password_here***
    ```

## Running Instructions 

1. On the target machine, run the following code to start the server:
```bash
cd SecurityComps2024/project/TargetMachine/backend
npm start
```
2. On the attacker machine, run the following code to run the tool:
```bash
cd SecurityComps2024/project/PasswordSprayingtool/
python3 password_spraying.py
```