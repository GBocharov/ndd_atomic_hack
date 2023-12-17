from langchain.schema import HumanMessage, SystemMessage
from giga_utils import chat

def get_answer_text(request, text):
    messages = [
        SystemMessage(
            content = "Задание: На основе текстов ниже ответь на вопрос, коротко если это возможно.\n"
                      "Вопрос : {} "
                      "Тексты : {}".format(request, text)
        )
    ]
    messages.append(HumanMessage(content=text))
    res1 = chat(messages)
    messages.append(res1)

    messages = [
        SystemMessage(
            content= "Задание : Выведи название файла, содержащего ответ на вопрос. \n"
                    "Вопрос : {} "
                    "Тексты : {}".format(request, text)
        )
    ]

    messages.append(HumanMessage(content=text))
    res2 = chat(messages)
    messages.append(res2)

    return res1.content +'\n'+ res2.content


def get_recommendation(text):
    messages = [
        SystemMessage(
            content = "Задача : коротко озаглавь текст ниже.\n" 
                      "Отрывок текста : {} ".format(text)
        )
    ]
    messages.append(HumanMessage(content=text))
    res = chat(messages)
    messages.append(res)
    return res.content


def get_answer_docs(request, docs):
    context = '\n'.join(  ['Текст {} : \n {}  \n Название документа: {}'.format(n, d[0].page_content, d[0].metadata['source']) for n, d in enumerate(docs)])

    res = get_answer_text(request, context)

    recs = []

    for i in docs:
        r = get_recommendation(i[0].page_content)
        recs.append(r)
    return res, recs

if __name__ == '__main__':
    ...