import re
import nltk
import pymorphy3

stop_words = ['и', 'в', 'во', 'он', 'на', 'я', 'с', 'со', 'а', 'то', 'о', 'все', 'она', 'так', 'его',
              'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от',
              'меня', 'еще',  'из', 'ему', 'теперь', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже',
              'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом',
              'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их',
              'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда',
              'этот', 'того', 'потому', 'этого',  'совсем', 'ним', 'здесь', 'этом', 'один', 'почти',
              'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при',
              'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про',
              'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой',
              'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю',
              'между', 'кто', 'какой', 'как', 'когда', 'что']

def prepare_text_for_embed(text):
    word_tokenizer = nltk.WordPunctTokenizer()
    regex = re.compile(r'[А-Яа-яёЁ0-9-]+')
    text = " ".join(regex.findall(text))
    tokens = word_tokenizer.tokenize(text)
    morph = pymorphy3.MorphAnalyzer()
    # удаляем стоп-слова, а так же лемитизируем слова
    tokens = [morph.parse(word)[0].normal_form.lower().replace('ё', 'е').replace('\\n\\', ' ') for word in tokens if (word not in stop_words)]
    tokens = [word.lower().replace('ё', 'е') for word in tokens if (word not in stop_words)]
    return ' '.join(tokens)

def prepare_text_for_db(text):
    word_tokenizer = nltk.WordPunctTokenizer()
    regex = re.compile(r'[А-Яа-яёЁ0-9-]+')
    text = " ".join(regex.findall(text))
    tokens = word_tokenizer.tokenize(text)
    return ' '.join(tokens)

def split_string_for_model(string, chunk_size):
    return [string[i : i + chunk_size] for i in range(0, len(string), chunk_size)]
