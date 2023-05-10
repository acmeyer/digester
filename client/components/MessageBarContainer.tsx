import React, { useRef, useState, useContext, FC } from "react";
import { DEFAULT_TEXTAREA_HEIGHT, MAX_TEXTAREA_HEIGHT } from "@/lib/constants";
import { PaperAirplaneIcon } from "@heroicons/react/24/solid";

type MessageBarProps = {
  addMessage: (message: string) => void;
  isAssistantResponding: boolean;
};

const MessageBarContainer: FC<MessageBarProps> = ({ addMessage, isAssistantResponding }) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [message, updateMessage] = useState("");

  const handleInputResize = (event: React.FormEvent<HTMLTextAreaElement>): void => {
    const target = event.currentTarget;
    target.style.height = "auto";
    if (target.scrollHeight > DEFAULT_TEXTAREA_HEIGHT) {
      target.style.height = `${target.scrollHeight}px`;
    }
  };

  const resetInputHeight = (): void => {
    if (textareaRef.current) {
      textareaRef.current.style.height = `${DEFAULT_TEXTAREA_HEIGHT}px`;
    }
  };

  const handleUpdateMessage = (event: React.FormEvent<HTMLTextAreaElement>): void => {
    const text = event.currentTarget.value;
    updateMessage(text);
  };

  const submitMessage = (): void => {
    if (isAssistantResponding || !message || !message.trim()) {
      return;
    }
    addMessage(message);
    updateMessage("");
    resetInputHeight();
  };

  return (
    <div className="fixed left-0 right-0 bottom-0 z-40 flex flex-col items-center gap-x-6 bg-gray-50 dark:bg-zinc-950">
      <div className="pb-8 px-4 md:px-0 pt-0 w-full relative flex flex-grow max-w-2xl lg:max-w-3xl items-center focus-within:z-10">
        <textarea
          ref={textareaRef}
          name="searchInput"
          id="searchInput"
          rows={1}
          style={{
            height: DEFAULT_TEXTAREA_HEIGHT,
            maxHeight: MAX_TEXTAREA_HEIGHT,
          }}
          className="pr-10 px-4 py-3 block w-full rounded-lg text-base text-gray-900 dark:text-white dark:bg-zinc-900 dark:border-zinc-800 border-gray-200 focus:ring-0 focus:ring-offset-0 focus:ring-offset-transparent focus:border-gray-300 dark:focus:border-zinc-700 focus:outline-none resize-none shadow-sm"
          placeholder={`Ask a question...`}
          value={message}
          onInput={handleInputResize}
          onChange={handleUpdateMessage}
          onKeyDown={(event) => {
            if (event.key === "Enter" && event.shiftKey === false) {
              submitMessage();
              event.preventDefault();
            }
          }}
        />
        <button
          type="button"
          className="absolute right-8 md:right-4 flex items-center justify-center cursor-point"
          onClick={() => submitMessage()}
          disabled={isAssistantResponding}
        >
          <PaperAirplaneIcon className="w-5 h-5 text-indigo-600 dark:text-gray-400" />
        </button>
      </div>
      <div className="w-full px-6">
      </div>
    </div>
  );
};

export default MessageBarContainer;
