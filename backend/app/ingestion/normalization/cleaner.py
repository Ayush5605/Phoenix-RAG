import re

class Cleaner:

    def clean(self,text:str)->str:

        text=text.replace("\r\n","\n")
        text=text.replace("\r","\n")

        text="\n".join(line.rstrip() for line in text.split("\n"))

        text=re.sub(r"\n{3,}","\n\n",text)

        return text.strip()


if __name__ == "__main__":

    cleaner = Cleaner()

    text = "Hello   \n\n\n\nWorld   \n\nThis is PhoenixRAG.   "

    cleaned_text = cleaner.clean(text)

    print("BEFORE:")
    print(repr(text))

    print("\nAFTER:")
    print(repr(cleaned_text))



