from readers.word_reader import WordReader
from ai.openai_matcher import OpenAIMatcher

reader = WordReader()

matcher = OpenAIMatcher()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

parameter = "Minimum Entry Age"

description = v1[
    "Minimum Entry Age"
]

prompt = matcher.build_prompt(

    parameter,

    description,

    v2

)

print(prompt)