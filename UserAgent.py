from uagents import Agent, Context, Protocol, Model
import asyncio

class DocumentUnderstanding(Model):
    pdf_path: str
    question: str
 
class DocumentsResponse(Model):
    learnings: str

# Add a simple state management class to track responses
class ResponseState:
    def __init__(self):
        self.waiting_for_response = False
        self.response_received = asyncio.Event()
    
    def set_waiting(self):
        self.waiting_for_response = True
        self.response_received.clear()
    
    def set_received(self):
        self.waiting_for_response = False
        self.response_received.set()
        
    async def wait_for_response(self, timeout=60):
        await asyncio.wait_for(self.response_received.wait(), timeout=timeout)

# Create a global state object
response_state = ResponseState()

user_agent = Agent(
    name="User Agent", 
    seed="User Agent Murakami", 
    port=8000, 
    endpoint=["http://127.0.0.1:8000/submit"]
)
 
@user_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {user_agent.name} and my address is {user_agent.address}.")
    ctx.logger.info("Welcome to the Haruki Murakami Style Simulation System.")
    ctx.logger.info(f"My address for messages is: {user_agent.address}")

summary_protocol = Protocol("Text Summarizer")
 
rag_agent = "agent1qg5p8542j5003zukhtkzvkr0y3hpg7nlk9e8wwv368r8705m8llq2ku6v27"

@user_agent.on_event("startup")
async def on_startup(ctx: Context):
    await user_interaction(ctx)

async def user_interaction(ctx: Context):
    """Handle user interaction"""
    while True:
        pdf_path = input("\nEnter PDF file path (default: ./norwegian.pdf): ")
        pdf_path = pdf_path if pdf_path else "./norwegian.pdf"
        
        question = input("Enter your question: ")
        if not question:
            continue
        
        ctx.logger.info(f"Analyzing document: {pdf_path}")
        ctx.logger.info(f"Your question: {question}")
        
        # Set state to waiting for response
        response_state.set_waiting()
        
        # Send query to RAG Agent
        await ctx.send(
            rag_agent,
            DocumentUnderstanding(pdf_path=pdf_path, question=question),
        )
        
        print("\nWaiting for Murakami-style response...\n")
        
        try:
            # Wait for the response with timeout
            await response_state.wait_for_response(timeout=120)
        except asyncio.TimeoutError:
            print("\n" + "="*50)
            print("Response timed out. The RAG agent may not be running or is having issues.")
            print("="*50 + "\n")
            # Continue the loop even if timeout occurs
 
@user_agent.on_message(model=DocumentsResponse)
async def document_load(ctx: Context, sender: str, msg: DocumentsResponse):
    ctx.logger.info(f"Received response from {sender}")
    print("\n" + "="*50)
    print("Murakami-style Response:")
    print("-"*50)
    print(msg.learnings)
    print("="*50 + "\n")
    
    # Set state to response received
    response_state.set_received()
 
user_agent.include(summary_protocol, publish_manifest=True)
user_agent.run()