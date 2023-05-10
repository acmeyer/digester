import useSWR from "swr";
import { fetcher } from "@/lib/helpers";
import { SERVER_ADDRESS } from "@/lib/constants";

export const useItems = () => {
  const { data, error, isLoading } = useSWR(
    `${SERVER_ADDRESS}/summaries`,
    fetcher
  );

  return {
    items: data?.items,
    isLoading,
    error,
  };
};