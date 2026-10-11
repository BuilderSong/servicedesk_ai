"""Optional download and inference. Review the model card and license first."""
import os
from transformers import pipeline
options = {"revision":os.environ["HF_REVISION"]} if os.getenv("HF_REVISION") else {}
classifier=pipeline("text-classification",model=os.environ["HF_MODEL"],device=-1,**options)
for text in ["Thank you for your help.","This is not good.","Please fix the urgent leak."]:
    print(text, classifier(text))
