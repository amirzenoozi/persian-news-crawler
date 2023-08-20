from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline


def sentiment_classifier(text):
    tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased-sentiment-deepsentipers-binary")
    model = AutoModelForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased-sentiment-deepsentipers-binary")

    model.eval()
    classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)
    
    return classifier(text)


def category_classifier(text):
    tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased-clf-persiannews")
    model = AutoModelForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased-clf-persiannews")

    model.eval()
    classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)
    
    return classifier(text)


if __name__ == '__main__':
    text = "ایران نوشت: مدتی قبل، مرد جوانی در حال عبور از خیابانی در پایتخت ناگهان با مرد سالخورده‌ای روبه‌رو شد که بی‌هوش کنار خیابان افتاده بود. مرد میانسال زخمی بود و به سختی نفس می‌کشید."
    print(category_classifier(text))
    print(sentiment_classifier(text))