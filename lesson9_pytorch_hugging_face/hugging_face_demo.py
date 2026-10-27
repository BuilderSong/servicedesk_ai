from transformers import pipeline

classifier = pipeline( # type: ignore
    task="sentiment-analysis", # type: ignore
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    device=-1,  # Run on the CPU.
)

messages = [
    "The repair was excellent. Thank you!",
    "I am very unhappy with the service.",
]

results = classifier(messages)

for message, result in zip(messages, results):
    print(f"Message: {message}")
    print(f"Sentiment: {result['label']}")
    print(f"Score: {result['score']:.3f}")
    print()