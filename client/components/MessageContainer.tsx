/* eslint-disable react/no-unstable-nested-components */
/* eslint-disable @next/next/no-img-element */
import { useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import Image from "next/image";
import { UserCircleIcon } from "@heroicons/react/24/solid";
import { MESSAGE_ROLES } from "@/lib/constants";

type MessageContainerProps = {
  message: any;
  messageComponent?: any;
};

function MessageContainer({ message, messageComponent }: MessageContainerProps) {
  const isAssistantMessage = useMemo(() => message.role === MESSAGE_ROLES.ASSISTANT, [message])

  return (
    <div 
      className={`relative sm:flex items-start dark:text-white text-gray-900 ${isAssistantMessage ? "" : "flex-row-reverse"}`}
    >
      <div className="relative mb-2">
        {isAssistantMessage ? (
          <Image
            className="flex items-center justify-center w-12 h-12 rounded-full"
            src="/logo.png"
            alt="avatar"
            width={48}
            height={48}
          />
        ) : (
          <UserCircleIcon className="flex items-center justify-center w-12 h-12 rounded-full text-gray-400 dark:text-zinc-500" />
        )}
      </div>
      <div 
        className={`min-w-0 flex-1 p-4 border border-gray-50 dark:border-zinc-800 rounded-lg lg:col-span-2 lg:row-span-2 space-y-2 bg-white dark:bg-zinc-900 shadow-sm ${isAssistantMessage ? "sm:ml-4" : "sm:mr-4"}`}
      >
        {messageComponent ? messageComponent() : (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            linkTarget="_blank"
            rehypePlugins={[() => rehypeHighlight({ detect: true })]}
            className="prose max-w-none break-words dark:prose-invert"
          >
            {message.text}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
}

export default MessageContainer;
