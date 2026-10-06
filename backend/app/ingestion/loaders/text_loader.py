from .base import DocumentLoader

class TextLoader(DocumentLoader):


    def load(self,file_path:str):
        with open(file_path,"r",encoding="utf-8") as f:
            text=f.read()

        return text


if __name__ == "__main__":
    loader = TextLoader()

    text = loader.load("app/ingestion/scanner/file_detector.py")

    print(text[:500])