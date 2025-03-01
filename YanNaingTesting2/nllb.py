from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

text = input("Add your question and i will give you my answer!")
checkpoint = "facebook/nllb-200-distilled-600M"
# # checkpoint = "facebook/nllb-200–1.3B"
# # checkpoint = "facebook/nllb-200–3.3B"
# # checkpoint = 'facebook/nllb-200-distilled-1.3B"

model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

target_lang = "mya_Mymr"
src_lang = "eng_Latn"

translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=src_lang, tgt_lang=target_lang, max_length = 100)

output = translator(text)
translated_text = output[0]["translation_text"]
print(translated_text)