from langchain_community.document_loaders import PyPDFLoader
from uagents import Agent, Context, Protocol, Model
from typing import List
 
 
class PDF_Request(Model):
    pdf_path: str
 
 
class PagesResponse(Model):
    pages: List
 
 
pdf_agent = Agent(
    name="PDF Agent",
    seed="PDF Agent Murakami",
    port=8003,
    endpoint=["http://127.0.0.1:8003/submit"],
)

@pdf_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {pdf_agent.name} and my address is {pdf_agent.address}.")

pdf_loader_protocol = Protocol("Text Summarizer")
 
 
@pdf_agent.on_message(model=PDF_Request, replies=PagesResponse)
async def document_load(ctx: Context, sender: str, msg: PDF_Request):
    loader = PyPDFLoader(msg.pdf_path)
    documents = loader.load_and_split()

    serializable_pages = []
    for doc in documents:
        serializable_pages.append({
            "page_content": doc.page_content,
            "metadata": doc.metadata
        })
    await ctx.send(sender, PagesResponse(pages=serializable_pages))
 
 
pdf_agent.include(pdf_loader_protocol, publish_manifest=True)
pdf_agent.run()
 