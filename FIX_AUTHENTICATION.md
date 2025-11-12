# Fix GitHub Authentication Error (401 Unauthorized)

## Problem
```
fatal: Response status code does not indicate success: 401 (Unauthorized).
```

This means GitHub rejected your credentials.

## Solution: Use Personal Access Token

GitHub no longer accepts passwords for HTTPS authentication. You MUST use a Personal Access Token.

### Step 1: Create Personal Access Token

1. **Go to GitHub Settings:**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub → Your Profile → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token:**
   - Click "Generate new token" → "Generate new token (classic)"
   - **Note:** `TimeGuard-Automation-Push`
   - **Expiration:** 90 days (or your preference)
   - **Select scopes:** ✅ Check **`repo`** (Full control of private repositories)
   - Click "Generate token" at the bottom

3. **Copy the Token:**
   - **IMPORTANT:** Copy the token immediately (starts with `ghp_...`)
   - You won't be able to see it again!

### Step 2: Clear Cached Credentials

**Windows:**
```bash
# Clear Windows Credential Manager
cmdkey /list
cmdkey /delete:git:https://github.com
```

Or use Git Credential Manager:
```bash
git credential-manager erase https://github.com
```

### Step 3: Push Again

```bash
git push -u origin main
```

**When prompted:**
- **Username:** `Pradeep-Kumar25th`
- **Password:** Paste your Personal Access Token (the `ghp_...` token you copied)

**Note:** Git will show "Password:" but paste your token there.

### Step 4: Save Credentials (Optional)

After successful push, Git will ask if you want to save credentials:
- Type `y` and press Enter
- This saves your token for future pushes

---

## Alternative: Use SSH (No Token Needed)

### Step 1: Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "prakumar@malomatia.com"
```

- Press Enter to accept default location
- Press Enter twice for no passphrase (or set one if you prefer)

### Step 2: Copy Public Key

```bash
type %USERPROFILE%\.ssh\id_ed25519.pub
```

Copy the entire output (starts with `ssh-ed25519`)

### Step 3: Add SSH Key to GitHub

1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. **Title:** `TimeGuard Automation - Windows PC`
4. **Key:** Paste your public key
5. Click "Add SSH key"

### Step 4: Change Remote to SSH

```bash
git remote set-url origin git@github.com:Pradeep-Kumar25th/TimeGuard-Automation.git
```

### Step 5: Test SSH Connection

```bash
ssh -T git@github.com
```

You should see: "Hi Pradeep-Kumar25th! You've successfully authenticated..."

### Step 6: Push

```bash
git push -u origin main
```

No password needed! ✅

---

## Quick Fix Commands

### Option A: HTTPS with Token (Recommended for beginners)

```bash
# 1. Clear old credentials
cmdkey /delete:git:https://github.com

# 2. Push (will prompt for username and token)
git push -u origin main
# Username: Pradeep-Kumar25th
# Password: [Paste your Personal Access Token]
```

### Option B: Switch to SSH (Recommended for security)

```bash
# 1. Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "prakumar@malomatia.com"

# 2. Copy public key
type %USERPROFILE%\.ssh\id_ed25519.pub
# Copy the output and add to GitHub Settings → SSH Keys

# 3. Change remote to SSH
git remote set-url origin git@github.com:Pradeep-Kumar25th/TimeGuard-Automation.git

# 4. Push
git push -u origin main
```

---

## Verify Authentication

After successful push, verify:

1. **Check repository:** https://github.com/Pradeep-Kumar25th/TimeGuard-Automation
2. **You should see all files:**
   - README.md
   - backend/ folder
   - app/ folder
   - components/ folder
   - All documentation files

---

## Troubleshooting

### "Permission denied (publickey)" (SSH)
- Make sure SSH key is added to GitHub
- Test connection: `ssh -T git@github.com`

### "Token has expired"
- Generate a new token
- Use the new token

### "Repository not found"
- Check repository name is correct
- Verify you have write access

### Still getting 401?
1. Double-check token has `repo` scope
2. Make sure you're using token, not password
3. Clear all cached credentials
4. Try SSH method instead

---

## Need Help?

If you're still having issues:
1. Try the SSH method (easier long-term)
2. Or use GitHub Desktop (GUI tool)
3. Check GitHub status: https://www.githubstatus.com/

