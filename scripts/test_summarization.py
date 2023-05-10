import argparse
from models.models import Message, MessageRole
from services.embeddings import query_embeddings
from services.summarize import create_summary
from services.chat_completion import setup_prompt, get_chat_completion


# To run directly on command line, run `python main.py`
if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-u", "--url", type=str, help="URL to summarize")
    argparser.add_argument("-f", "--filepath", type=str, help="Path to file to summarize")
    argparser.add_argument("-m", "--model", type=str, help="Model to use", default="gpt-4")
    argparser.add_argument("-s", "--summary_type", type=str, help="Type of summary to generate", default="short")
    args = argparser.parse_args()
    url = args.url
    summary_type = args.summary_type
    filepath = args.filepath
    model = args.model

    assert url or filepath, "Must provide either a URL or a filepath"

    summary_response = create_summary(url, filepath, summary_type, model)
    print(summary_response.summary)

    conversation_messages = []
    prompt = setup_prompt('prompts/chat_prompt.md')
    item_details = f"Title: {summary_response.title}\nSummary: {summary_response.summary}"
    prompt = prompt.replace("$item_information", item_details)
    while (user_input := input('You: ').strip()) != "":
        relevant_docs = query_embeddings(query=user_input, item_id=summary_response.id, top_k=3)
        relevant_content = "\n\n".join([f"{doc.get('metadata').get('text')}" for doc in relevant_docs])
        user_content = f"""
        Relevant content:
        {relevant_content}
        =====
        {user_input}
        """
        user_message = Message(role=MessageRole.user, content=user_content)
        conversation_messages.append(user_message)
        answer = get_chat_completion(prompt, messages=conversation_messages)
        conversation_messages.append(Message(role=MessageRole.assistant, content=answer))
        print(f'\nBot: {answer}\n')
