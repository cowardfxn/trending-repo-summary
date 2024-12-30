# GitHub Trending Daily Report Generator
Generate GitHub Trending Repos report with ollama local service, or ZhipuAI.


## Step 0: Set PYTHONPATH

```bash
export PYTHONPATH=.
```

Or

```powershell
$env:PYTHONPATH = "."
```

## Step 1: Install dependencies

`pip install -r requirements.txt`

## Commands

### Docker Setup

Docker Hub alternatives.

```bash
docker pull docker.1ms.run/ollama/ollama

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama docker.1ms.run/ollama/ollama
```

### Pull models
```
ollama pull llava
```

### Run models

```
ollama run llama3.2
```

#### Available models on local container
 - llama3.2
 - llava
 - llama3.2-vision (requires 11.6GB memory)


## Generate reports

`python start.py`

The new HTML file is created in project root directory.
