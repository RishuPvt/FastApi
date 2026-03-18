from langchain.agents import initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_groq import ChatGroq
from agent.tool import search_products, add_to_cart, remove_from_cart , cart_total , clear_cart , login_user , view_cart , update_cart_quantity
from dotenv import load_dotenv


load_dotenv()

llm =ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
# llm = model1 = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0
# )
tools = [
    search_products,
    add_to_cart,
    remove_from_cart ,
    cart_total ,
    clear_cart ,
     login_user ,
     view_cart ,
     update_cart_quantity
]

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "system_message": """
You are an ecommerce assistant.

When performing actions you MUST use tools.

Format strictly:

Thought: what you think
Action: tool name
Action Input: input for tool

Available tools:
search_products
add_to_cart
remove_from_cart
"""
    }
)

