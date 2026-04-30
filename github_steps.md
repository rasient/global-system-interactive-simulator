# GitHub upload steps

## 1. Create the repository

Go to GitHub → New repository

Repository name:

```text
global-system-interactive-simulator
```

Description:

```text
Interactive Streamlit simulator for exploring AI, labor, infrastructure, trust, incentives, and coordination dynamics.
```

Choose Public.

## 2. Upload files

Upload these files:

```text
app.py
requirements.txt
README.md
github_steps.md
```

## 3. Commit

Commit message:

```text
Initial interactive simulator
```

## 4. Run locally

```powershell
pip install -r requirements.txt
streamlit run app.py
```

## 5. Deploy on Streamlit Cloud

1. Go to Streamlit Community Cloud
2. Connect GitHub
3. Select this repository
4. Main file path:

```text
app.py
```

5. Deploy
