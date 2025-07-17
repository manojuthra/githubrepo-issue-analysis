from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import requests
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class AnalyzeRequest(BaseModel):
    repo_url: str
    issue_number: int

# Helper to parse owner/repo from URL
def parse_github_repo(url: str):
    parts = url.rstrip('/').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub repo URL")
    return parts[-2], parts[-1]

# Fetch issue data from GitHub
def fetch_issue(owner: str, repo: str, issue_number: int):
    headers = {"Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Issue not found")
    issue = r.json()
    # Fetch comments
    comments_url = issue.get("comments_url")
    comments = []
    if comments_url:
        cr = requests.get(comments_url, headers=headers)
        if cr.status_code == 200:
            comments = cr.json()
    return issue, comments

# Placeholder for LLM call
def analyze_with_llm(issue: Dict[str, Any], comments: Any) -> Dict[str, Any]:
    prompt = f"""
You are an AI assistant. Analyze the following GitHub issue and comments. Output a JSON with the following fields:\n\nsummary: A one-sentence summary of the user's problem or request.\ntype: Classify the issue as one of the following: bug, feature_request, documentation, question, or other.\npriority_score: A score from 1 (low) to 5 (critical), with a brief justification for the score.\nsuggested_labels: An array of 2-3 relevant GitHub labels (e.g., 'bug', 'UI', 'login-flow').\npotential_impact: A brief sentence on the potential impact on users if the issue is a bug.\n\nIssue Title: {issue.get('title')}\nIssue Body: {issue.get('body')}\nComments: {comments}\n\nRespond ONLY with the JSON object.\n"""
    try:
        print(OPENAI_API_KEY)
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )
        content = response.choices[0].message.content
        import json
        return json.loads(content)
    except Exception as e:
        # Fallback: return dummy response
        return {
            "summary": "Example summary.",
            "type": "bug",
            "priority_score": "3 - Medium impact, affects some users.",
            "suggested_labels": ["bug", "UI"],
            "potential_impact": "Users may experience UI glitches.",
            "error": str(e)
        }

@app.post("/analyze_issue")
def analyze_issue(req: AnalyzeRequest):
    try:
        owner, repo = parse_github_repo(req.repo_url)
        issue, comments = fetch_issue(owner, repo, req.issue_number)
        result = analyze_with_llm(issue, comments)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 