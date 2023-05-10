import useSWR from "swr";
import { fetcher } from "@/lib/helpers";
import { SERVER_ADDRESS } from "@/lib/constants";

export const useConversation = (itemId: string) => {
  const { data, error, isLoading } = useSWR(
    `${SERVER_ADDRESS}/summaries/${itemId}/messages`,
    fetcher
  );

  return {
    messages: data?.messages,
    isLoading,
    error,
  };
};