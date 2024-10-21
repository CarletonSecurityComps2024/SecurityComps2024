# Building-Hacking-Tools-From-Scratch

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
