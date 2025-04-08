from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from uagents import Agent, Context, Protocol, Model
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate  # Updated import
from langchain_core.runnables import RunnablePassthrough  # Added for modern chaining
from typing import List
import os
import uuid
import faiss
import asyncio
 
class PDF_Request(Model):
    pdf_path: str
 
class DocumentUnderstanding(Model):
    pdf_path: str
    question: str
 
class PagesResponse(Model):
    pages: List
 
class DocumentsResponse(Model):
    learnings: str
 
rag_agent = Agent(
    name="RAG Agent",
    seed="RAG Agent Murakami",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)
 
@rag_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {rag_agent.name} and my address is {rag_agent.address}.")
    ctx.logger.info("I analyze Haruki Murakami's writing style and generate similar responses.")
    ctx.logger.info(f"Configured to send responses to user agent: {user_agent}")

faiss_protocol = Protocol("FAISS")
 
user_agent = "agent1qv2fy5gya5fvzhkszgf87sjj5z7nkp5027yq94ya6q4g4n0rp7sev8tefj7"
pdf_agent = "agent1q0cwtd2lcyzcme34j27hn6anw5k50lp0r2ss2jdwsrkc99l97kkp596ycjl"
 
openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_api_key)
llm = ChatOpenAI(temperature=0.7, model="gpt-4o", openai_api_key=openai_api_key)

# Enhanced Murakami style prompt template
murakami_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are embodying the literary voice of Haruki Murakami, the renowned Japanese author. Your task is to respond to questions in his distinctive writing style, using the provided context as reference material.

### CONTEXT INFORMATION:
{context}

### QUESTION TO ANSWER:
{question}

### HARUKI MURAKAMI STYLE GUIDELINES:
1. SENTENCE STRUCTURE:
   - Favor short to medium length sentences with occasional longer ones for rhythm
   - Use simple vocabulary but arrange it in unexpected combinations
   - Employ first-person narration when appropriate, with a contemplative tone

2. TONAL QUALITIES:
   - Maintain a detached, almost clinical observation of emotional states
   - Balance melancholy with subtle humor and matter-of-fact acceptance
   - Present the surreal or bizarre as if completely ordinary

3. THEMATIC ELEMENTS TO INCORPORATE:
   - Loneliness and isolation as persistent conditions of modern life
   - The thin boundary between reality and parallel worlds
   - Unresolved mysteries that don't require solutions
   - The significance of small, mundane details and routines

4. DISTINCTIVE MURAKAMI ELEMENTS:
   - References to Western music (especially jazz, classical, or Beatles)
   - Food preparation or eating described in methodical detail
   - Cats or other animals that may possess mysterious qualities
   - Wells, corridors, or other transitional spaces as metaphors

5. IMAGERY AND METAPHOR:
   - Use simple but vivid sensory descriptions
   - Employ unexpected similes that create cognitive dissonance
   - Allow certain images to remain intentionally ambiguous

### EXAMPLE MURAKAMI PHRASINGS:
- "The answer is floating somewhere, but I can't quite catch it - like trying to grab smoke with your bare hands."
- "That's just how it is sometimes. The world has its own logic that doesn't need to match ours."
- "I poured another whisky, letting the ice crack and settle like distant thoughts rearranging themselves."

Now, compose your response in Murakami's style, addressing the question while incorporating relevant details from the context:
"""
)
 
@rag_agent.on_message(model=DocumentUnderstanding, replies=PDF_Request)
async def document_load(ctx: Context, sender: str, msg: DocumentUnderstanding):
    ctx.logger.info(f"Received question: {msg.question}")
    ctx.storage.set(str(ctx.session), {"question": msg.question, "sender": sender})
    await ctx.send(
        pdf_agent, PDF_Request(pdf_path=msg.pdf_path)
    )
 
@rag_agent.on_message(model=PagesResponse, replies=DocumentsResponse)
async def document_understand(ctx: Context, sender: str, msg: PagesResponse):
    ctx.logger.info("Received PDF content, processing...")
    # Create index
    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello")))
 
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
 
    documents = []
    for page in msg.pages:
        documents.append(
            Document(page_content=page["page_content"], metadata=page["metadata"])
        )
 
    uuids = [str(uuid.uuid4()) for _ in range(len(documents))]
 
    vector_store.add_documents(documents=documents, ids=uuids)
 
    prev = ctx.storage.get(str(ctx.session))
    question = prev["question"]
    response_recipient = prev["sender"]
    
    ctx.logger.info(f"Will send response to: {response_recipient}")
    
    # Optimize retrieval - increase retrieval count
    results = vector_store.similarity_search(
        question,
        k=4,  # Increased document count
    )
 
    if len(results) > 0:
        # Combine retrieval results
        context = "\n\n".join([doc.page_content for doc in results])
        
        # Use new LangChain syntax instead of deprecated LLMChain
        chain = (
            {"context": RunnablePassthrough(), "question": lambda _: question} 
            | murakami_prompt 
            | llm
        )
        
        try:
            # Use invoke instead of run
            response = chain.invoke(context)
            
            # Extract the content from the response (ChatOpenAI returns a message object)
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            ctx.logger.info("Generated Murakami-style response:")
            ctx.logger.info(response_text)
            
            # Explicitly log the recipient address
            ctx.logger.info(f"Attempting to send response to {response_recipient}")
            
            # Add retry logic for connection issues
            max_retries = 5  # Increase retry count
            for retry in range(max_retries):
                try:
                    await ctx.send(
                        response_recipient, DocumentsResponse(learnings=response_text)
                    )
                    ctx.logger.info(f"Successfully sent response to {response_recipient}")
                    break
                except Exception as e:
                    ctx.logger.warning(f"Failed to send response (attempt {retry+1}/{max_retries}): {e}")
                    if retry < max_retries - 1:
                        wait_time = 2 * (retry + 1)  # Exponential backoff
                        ctx.logger.info(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        ctx.logger.error(f"Could not deliver response after {max_retries} attempts")
        except Exception as e:
            ctx.logger.error(f"Error generating response: {e}")
            await ctx.send(
                response_recipient, DocumentsResponse(learnings=f"An error occurred while processing your request: {str(e)}")
            )
    else:
        await ctx.send(
            response_recipient, DocumentsResponse(learnings="I'm sorry, I couldn't find relevant information in the document. Like cherry blossoms falling silently, some questions are destined to remain unanswered.")
        )
 
rag_agent.include(faiss_protocol, publish_manifest=True)
rag_agent.run()
