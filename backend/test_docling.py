from app.ingestion.loaders.docling_loader import DoclingLoader


loader = DoclingLoader()

document = loader.load("../dataset/data/Engineer/API/fastapi/README.md")

print(document)