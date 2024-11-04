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
