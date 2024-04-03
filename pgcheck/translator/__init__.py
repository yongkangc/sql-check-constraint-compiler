from pgcheck.translator.translator import Translator


def perform_translation(sql: str):
    translator = Translator()
    translator.translate(sql)
