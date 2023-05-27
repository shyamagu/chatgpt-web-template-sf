# .env
```
AOAI_OPENAI_KEY={Azure OpenAI Services apikey}
AOAI_ENDPOINT={Azure OpenAI Services endpoint}
AOAI_MODEL={gpt-35-turbo modelname}
AOAI_EMB_MODEL={embedding-ada-002 modelname}

BING_API_KEY={Bing Search v7 apikey}

FORM_REC_ENDPOINT={Azure Form Recognizer endpoint}
FORM_REC_KEY={Azure Form Recognizer apikey}

```
# requirement
```
pip install requirements.txt
```

# debug run
```
uvicorn main:app --reload
```