import MainTemplate from "@/components/MainTemplate"
import GetSummaryForm from "@/components/GetSummaryForm"

export default function CreateSummary() {
  return (
    <MainTemplate>
      <div className="flex items-center text-left flex-col">
        <div className="max-w-lg sm:max-w-xl lg:max-w-3xl w-full py-6 space-y-2 text-gray-900 dark:text-white">
          <h3>Add New Item</h3>
          <p className="text-sm">
            Upload your file or add a url to get a summary.
          </p>

          <GetSummaryForm />
        </div>
      </div>
    </MainTemplate>
  )
}
