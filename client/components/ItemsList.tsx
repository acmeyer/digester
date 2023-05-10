/* eslint-disable @next/next/no-img-element */
'use client'

import LoadingContainer from "./LoadingContainer"
import ErrorState from "./ErrorState"
import { useItems } from "@/hooks/items"
import Link from "next/link"
import EmptyState from "./EmptyState"

const ItemsList = () => {
  const { items, isLoading, error } = useItems()

  return (
    <div className="flex flex-1">
      {isLoading && (
        <div className="w-full">
          <LoadingContainer size="large" />
        </div>
      )}
      {error && (
        <div className="w-full">
          <ErrorState title="Error" text={error.message} />
        </div>
      )}
      {(!items && !isLoading && !error) || items?.length === 0 ? (
        <div className="w-full py-10">
          <EmptyState />
        </div>
      ) : (
        <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
          {items?.map((item: any) => (
            <Link href={`/summaries/${item.id}`} key={item.id}>
              <div className="group relative bg-white dark:bg-zinc-900 p-4 rounded-lg shadow-sm">
                <div className="min-h-40 aspect-h-1 aspect-w-1 w-full overflow-hidden rounded-md lg:aspect-none group-hover:opacity-75 lg:h-40">
                  <img
                    src={item?.item_metadata?.image}
                    alt={item?.item_metadata?.title}
                    className="h-full w-full object-cover object-center lg:h-full lg:w-full"
                  />
                </div>
                <div className="mt-4 flex justify-between">
                  <div>
                    <h3 className="text-sm text-gray-700 dark:text-gray-50">
                      <span aria-hidden="true" className="absolute inset-0" />
                      {item?.item_metadata?.title}
                    </h3>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default ItemsList;