
from enum import Enum
from pathlib import Path

class FileType(Enum):
    PDF="pdf"
    MARKDOWN="markdown" 
    TEXT="text"
    HTML="html"
    DOCX="docx"
    PPTX="pptx"
    XLSX="xlsx"
    IMAGE="image"
    UNKNOWN="unknown"
    PYTHON="python"
    JAVASCRIPT="javascript"
    TYPESCRIPT="typescript"
    JSON="json"
    YAML="yaml"
    SVG="svg"

EXTENSION_MAP={
    ".pdf":FileType.PDF,
    ".md":FileType.MARKDOWN,
    ".txt":FileType.TEXT,
    ".html":FileType.HTML,
    ".htm":FileType.HTML,
    ".docx":FileType.DOCX,
    ".pptx":FileType.PPTX,
    ".xlsx":FileType.XLSX,
    ".jpg":FileType.IMAGE,
    ".jpeg":FileType.IMAGE,
    ".png":FileType.IMAGE,
    ".py": FileType.PYTHON,

    ".js": FileType.JAVASCRIPT,
    ".jsx": FileType.JAVASCRIPT,

    ".ts": FileType.TYPESCRIPT,
    ".tsx": FileType.TYPESCRIPT,

    ".json": FileType.JSON,

    ".yaml": FileType.YAML,
    ".yml": FileType.YAML,

    ".svg": FileType.SVG

}

class FileDetector:

    def detect(self,file_path:str)->FileType:

        path=Path(file_path)
        extension=path.suffix.lower()

        return EXTENSION_MAP.get(extension,FileType.UNKNOWN)

if __name__=="__main__":
    detector=FileDetector()

    print(detector.detect("document.pdf"))
    print(detector.detect("README.MD"))
    print(detector.detect("image.jpg"))
    print(detector.detect("data.xlsx"))
    print(detector.detect("script.py"))
    print(detector.detect("script.py"))
    print(detector.detect("app.js"))
    print(detector.detect("component.jsx"))
    print(detector.detect("config.json"))
    print(detector.detect("docker-compose.yml"))
    print(detector.detect("image.svg"))