import useSWR from "swr";
import { fetcher } from "@/lib/helpers";
import { SERVER_ADDRESS } from "@/lib/constants";

export const useSummary = (summaryId: string) => {
  const { data, error, isLoading } = useSWR(
    `${SERVER_ADDRESS}/summaries/${summaryId}`,
    fetcher
  );

  return {
    summary: data?.item,
    isLoading,
    error,
  };
};