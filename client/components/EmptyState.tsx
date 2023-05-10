import Link from 'next/link';
import { ArrowDownCircleIcon } from '@heroicons/react/24/outline';
import { PlusIcon } from '@heroicons/react/20/solid';

export default function EmptyState() {
  return (
    <div className="text-center">
      <ArrowDownCircleIcon className="mx-auto h-12 w-12 text-gray-400" aria-hidden="true" />
      <h3 className="mt-2 text-sm font-semibold">No Items</h3>
      <p className="mt-1 text-sm text-gray-500 dark:text-gray-300">Get started by adding a new item.</p>
      <div className="mt-6">
        <Link
          href="/summaries/new"
          className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        >
          <PlusIcon className="-ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
          Add Item
        </Link>
      </div>
    </div>
  )
}