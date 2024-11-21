# Building-Hacking-Tools-From-Scratch

## [Presentation Poster Link](https://www.canva.com/design/DAGU2-71zNA/bffINJa6wHMd0bibsoQkyQ/edit?utm_content=DAGU2-71zNA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## How to run Password Spraying Tool

### Step 1: Target Machine

```bash
cd TargetMachine/backend
npm install
node server.js
```

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
5. Start up the target machine [instruction above]
6. Run the tool:
```bash
python3 password_spraying.py
```