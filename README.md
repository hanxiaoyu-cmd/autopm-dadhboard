# AutoPM 部署指南 / Deployment Guide

---

## 🇨🇳 中文指南

### 第一步：注册 GitHub

1. 打开 https://github.com 注册账号
2. 点击右上角 **+** → **New repository**
3. 仓库名填 `autopm`
4. 选择 **Private**（推荐，只有你能看到）
5. **不要勾选** "Add a README file"
6. 点击 **Create repository**

### 第二步：上传代码

**方式 A：网页上传（最简单）**

1. 在刚创建的仓库页面，点击 **uploading an existing file**
2. 把 `autopm-deploy/` 文件夹里的所有文件和文件夹拖进去
3. 确保文件结构如下：
   ```
   autopm/
   ├── backend/
   │   ├── main.py
   │   ├── models.py
   │   ├── schemas.py
   │   ├── auth.py
   │   ├── alerts_engine.py
   │   ├── database.py
   │   ├── seed.py
   │   ├── requirements.txt
   │   └── Procfile
   ├── frontend/
   │   └── index.html
   ├── render.yaml
   └── README.md
   ```
4. 点击 **Commit changes**

**方式 B：Git 命令行**

```bash
cd autopm-deploy
git init
git add .
git commit -m "Initial commit: AutoPM"
git remote add origin https://github.com/你的用户名/autopm.git
git push -u origin main
```

### 第三步：注册 Render 并部署

1. 打开 https://render.com 点击 **Get Started**（可以用 GitHub 账号登录）
2. 登录后，点击 **New** → **Web Service**
3. 选择 **Build and deploy from a Git repository**
4. 点击 **Connect** 连接你的 GitHub 仓库 `autopm`
5. 填写部署设置：
   - **Name**: `autopm`（或你喜欢的名字）
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
6. 点击 **Create Web Service**

### 第四步：等待部署完成

- 大约 3-5 分钟
- 你可以在 Render 的 **Logs** 页面看到部署进度
- 部署完成后，Render 会给你一个 URL，类似 `https://autopm-xxxx.onrender.com`
- 打开这个 URL 就能看到 AutoPM 了！

### 第五步：分享给团队

- 把 URL 发给 3-5 个人
- 所有人改的数据实时同步到同一个数据库
- 默认管理员账号：用户名 `sunny`，密码 `autopm2026`
- **免费套餐限制**：30 分钟没人访问会休眠，有人访问自动唤醒（等待约 30 秒）

### ⚠️ 注意事项

- 免费套餐的 SQLite 数据库在每次部署时会重置。如果需要持久化数据，建议升级到 Render 付费套餐或使用外部数据库。
- 免费套餐每月有 750 小时免费运行时间。
- 如果页面加载慢，是后端正在唤醒（从休眠到启动约 30 秒）。

---

## 🇺🇸 English Guide

### Step 1: Register GitHub

1. Go to https://github.com and sign up
2. Click **+** → **New repository** in the top right
3. Repository name: `autopm`
4. Select **Private** (recommended)
5. Do **NOT** check "Add a README file"
6. Click **Create repository**

### Step 2: Upload Code

**Option A: Web Upload (Easiest)**

1. On your new repository page, click **uploading an existing file**
2. Drag all files and folders from the `autopm-deploy/` directory
3. Make sure the structure looks like:
   ```
   autopm/
   ├── backend/
   │   ├── main.py
   │   ├── models.py
   │   ├── schemas.py
   │   ├── auth.py
   │   ├── alerts_engine.py
   │   ├── database.py
   │   ├── seed.py
   │   ├── requirements.txt
   │   └── Procfile
   ├── frontend/
   │   └── index.html
   ├── render.yaml
   └── README.md
   ```
4. Click **Commit changes**

**Option B: Git CLI**

```bash
cd autopm-deploy
git init
git add .
git commit -m "Initial commit: AutoPM"
git remote add origin https://github.com/YOUR_USERNAME/autopm.git
git push -u origin main
```

### Step 3: Register Render & Deploy

1. Go to https://render.com and click **Get Started** (you can sign in with GitHub)
2. After login, click **New** → **Web Service**
3. Select **Build and deploy from a Git repository**
4. Click **Connect** next to your `autopm` repository
5. Fill in deployment settings:
   - **Name**: `autopm` (or any name you like)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
6. Click **Create Web Service**

### Step 4: Wait for Deployment

- Takes about 3-5 minutes
- You can check progress in Render's **Logs** page
- Once deployed, Render gives you a URL like `https://autopm-xxxx.onrender.com`
- Open that URL and you'll see AutoPM!

### Step 5: Share with Team

- Share the URL with 3-5 people
- All changes sync in real-time to the same database
- Default admin account: username `sunny`, password `autopm2026`
- **Free tier note**: The service sleeps after 30 min of inactivity. It auto-wakes when someone visits (takes ~30 seconds).

### ⚠️ Important Notes

- On the free tier, the SQLite database resets on each deployment. For persistent data, consider upgrading Render or using an external database.
- Free tier includes 750 hours/month of runtime.
- If the page loads slowly, the backend is waking up from sleep (~30 seconds).
