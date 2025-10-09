##
Installation (Conda + uv)
```
conda create -n <env_name> python=3.11
conda activate <env_name>

pip install uv

uv pip install -r requirements.txt
```

Run pytest
```
pytest -v
```