# GitHub Issue Analyzer

## Overview
This app analyzes GitHub issues using AI. Enter a public GitHub repo URL and issue number, and get a structured analysis.

## Setup

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set your OpenAI API key (optional, for real LLM integration)
set OPENAI_API_KEY=sk-...your-key...  # On Windows
export OPENAI_API_KEY=sk-...your-key...  # On Mac/Linux

# Run the FastAPI server
uvicorn main:app --reload
```

### 2. Frontend (Streamlit)

```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## Usage
- Open the Streamlit app in your browser (usually at http://localhost:8501)
- Enter a GitHub repo URL (e.g., https://github.com/facebook/react) and an issue number
- Click "Analyze Issue" to see the AI-generated analysis

## Notes
- The backend currently returns a dummy response. Integrate with OpenAI or another LLM for real analysis.
- Both backend and frontend must be running for the app to work. 

If you are still getting the 401 error after setting your API key, here are the most common causes and solutions:

---

## 1. Double-check the API Key

- Make sure you copied the **entire** API key from OpenAI, with no extra spaces or missing characters.
- The key should start with `sk-` and be quite long (about 51 characters).

---

## 2. Set the Environment Variable Correctly

**For Windows (PowerShell or Command Prompt):**
```sh
set OPENAI_API_KEY=sk-your-real-key-here
```
- Run this command in the same terminal window where you will start your FastAPI server.
- Then, start your server in the same terminal.

**For Windows PowerShell (alternative):**
```sh
<code_block_to_apply_changes_from>
```

**For Mac/Linux:**
```sh
export OPENAI_API_KEY=sk-your-real-key-here
```
- Then, start your server in the same terminal.

---

## 3. Restart the Backend

- After setting the environment variable, you **must** restart your FastAPI server so it picks up the new variable.

---

## 4. Check for Hardcoded or Cached Keys

- Make sure you are not accidentally hardcoding the placeholder key (`sk-...your-key...`) anywhere in your code or `.env` files.
- In `backend/main.py`, this line:
  ```python
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...your-key...")
  ```
  will use the environment variable if set, but if not, it falls back to the placeholder. If your environment variable is not set, it will always use the placeholder and fail.

---

## 5. Print the Key for Debugging (Optional)

Add a print statement in your `backend/main.py` to check what key is being used (be careful not to share this output):

```python
print("OPENAI_API_KEY:", OPENAI_API_KEY)
```
- This should print your real key (or at least the first few and last few characters).
- If it prints the placeholder, your environment variable is not set correctly.

---

## 6. Virtual Environments

- If you are using a virtual environment, make sure you set the environment variable **after activating** the virtual environment and before starting the server.

---

## 7. API Key Permissions

- Make sure your API key is active and not restricted or deleted in your OpenAI dashboard.

---

### If you try all of the above and it still fails:

- Please copy and paste the exact commands you are using to set the environment variable and to start your server.
- Let me know if you are using Command Prompt, PowerShell, or another shell.

I can then give you step-by-step instructions tailored to your setup! 