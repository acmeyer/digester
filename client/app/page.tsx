import MainTemplate from "@/components/MainTemplate"
import ItemsList from "@/components/ItemsList"

export default function Home() {
  return (
    <MainTemplate>
      <div className="flex min-h-full flex-1 flex-col justify-center py-6">
        <h3>Items</h3>
        <ItemsList />
      </div>
    </MainTemplate>
  )
}
