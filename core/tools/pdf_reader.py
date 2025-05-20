import os
from langchain.tools import tool
# from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader


@tool
def read_company_bio() -> str:
    """Reads the company bio from the PDF file and returns text content."""
    try:
        pdf_path = "company_bio.pdf"

        if not os.path.isfile(pdf_path):
            return f"Error: PDF file not found at {pdf_path}"

        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()

        print(f"Loaded {len(pages)} pages from {pdf_path}")
        return "\n\n".join(page.page_content for page in pages)
    except Exception as e:
        return f"Error reading PDF: {e}"
