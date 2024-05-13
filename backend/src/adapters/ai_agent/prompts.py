grammar_template = """
    Correct just the grammatical errors of “Text:” in standard English and place the result as the answer.
    Please, I want the given text back as similar as possible to the original text, but perfectly written
    in standard English.:
     Text: {input}
"""


style_template = """
    Change the style of “Text:” according the following rules “Style:” and place the result as the answer:
     Text: {input}
     Style: {style}
"""

summarization_default_template = """
    Please provide a summary of “Text:”

     Text: {input}
"""
