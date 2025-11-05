# MedChat

## Steps to run the project

```bash
# For Windows
python -m venv venv
```

```bash
# For Windows
venv/Scripts/activate
```
```bash
pip install -r requirements.txt
```

### Create a `.env` file in the root directory and add your Pinecone credentials as follows:

```ini
PINECONE_API_KEY = ""
PINECONE_API_ENV = ""
```

### Download the quantized model from the link provided in model folder and keep the model in the model directory:

```ini
## Download the Llama 2 Model:
llama-2-7b-chat.ggmlv3.q4_0.bin

# From the following link:
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML
```