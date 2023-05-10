/* eslint-disable @next/next/no-img-element */
'use client'

import LoadingContainer from "@/components/LoadingContainer";
import { useSummary } from "@/hooks/summaries"
import ErrorState from "./ErrorState";
import ConversationView from "./ConversationView";

export default function ItemDetails({ itemId }: { itemId: string }) {
  const { summary, isLoading, error } = useSummary(itemId);

  if (isLoading) return <LoadingContainer size="large" />;
  if (error) return <ErrorState title="Error" text={error.message} />;

  return (
    <div className="py-5 h-full max-w-2xl lg:max-w-3xl mx-auto">
      <div className="sm:flex">
          {summary?.item_metadata?.image && summary.item_metadata.image !== "" && (
            <div className="mb-4 flex-shrink-0 sm:mb-0 sm:mr-4">
              <img 
                src={summary.item_metadata.image} 
                alt={summary.item_metadata.title} 
                className="h-32 w-full border border-gray-300 bg-white text-gray-300" />
            </div>
          )}
        <div>
          <h4 className="text-xl font-bold">
            {summary?.item_metadata?.title}
          </h4>
          {summary?.item_metadata?.author && summary.item_metadata.author !== '' && (
            <p className="text-xs mt-1 text-gray-500 dark:text-gray-400">
              by {summary?.item_metadata?.author}
            </p>
          )}
          <p className="mt-1">
            <a className="text-blue-500 hover:underline text-xs" target="_blank" href={summary?.source_url}>
              View Original Source
            </a>
          </p>
        </div>
      </div>

      <ConversationView item={summary} />
    </div>
  )
}