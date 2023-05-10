import { useRef, useEffect, useState } from "react";
import MessageContainer from "./MessageContainer";
import MessageBarContainer from "./MessageBarContainer";
import LoadingContainer from "./LoadingContainer";
import ErrorState from "./ErrorState";
import { useConversation } from "@/hooks/conversations";
import { v4 as uuidv4 } from "uuid";
import { MESSAGE_ROLES, SERVER_ADDRESS } from "@/lib/constants";

const ConversationView = ({ item }: any) => {
  const bottomRef = useRef<HTMLDivElement>(null);
  const [isAssistantResponding, setIsAssistantResponding] = useState(false);
  const { messages, isLoading, error } = useConversation(item.id);
  const [currentConversationMessages, setCurrentConversationMessages] = useState<any>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "auto" });
  }, [currentConversationMessages]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "auto" });
    setCurrentConversationMessages(messages);
  }, [messages]);

  const onAddNewMessage = async (message: string) => {
    console.log(message);
    // First add the message to the local conversation
    setCurrentConversationMessages((prevConversationMessages: []) => {
      if (!prevConversationMessages) {
        return prevConversationMessages;
      }
      const conversationMessages = prevConversationMessages ? prevConversationMessages : [];
      return [
        ...conversationMessages,
        {
          id: uuidv4(),
          role: MESSAGE_ROLES.USER,
          text: message,
          created_at: new Date(),
        },
      ];
    });
    // Then add the message to the server conversation
    setIsAssistantResponding(true);
    const response = await fetch(`${SERVER_ADDRESS}/summaries/${item.id}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
      }),
    });
    const data = await response.json();
    setCurrentConversationMessages(data.messages);
    setIsAssistantResponding(false);
  };

  return (
    <>
      <div className="mt-5 space-y-5">
        {isLoading && (<LoadingContainer size="large" />)}
        {error && (<ErrorState title="Error" text={error.message} />)}
        {currentConversationMessages?.map((message: any) => (
          <MessageContainer key={message.id} message={message} />
        ))}
        {isAssistantResponding && (
          <MessageContainer 
            message={{ role: MESSAGE_ROLES.ASSISTANT, text: "" }} 
            messageComponent={() => (
              <div className="typing pl-1">
                <div className="min-h-7">
                  <span className="typing__dot" />
                  <span className="typing__dot" />
                  <span className="typing__dot" />
                </div>
              </div>
            )}
          />
        )}
        <div className="h-20" ref={bottomRef} />
      </div>
      <MessageBarContainer addMessage={onAddNewMessage} isAssistantResponding={isAssistantResponding} />
    </>
  )
}

export default ConversationView;