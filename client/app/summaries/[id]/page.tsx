import MainTemplate from "@/components/MainTemplate"
import ItemDetails from "@/components/ItemDetails"

export default function SummaryPage({ params }: { params: { id: string } }) {
  return (
    <MainTemplate>
      <ItemDetails itemId={params.id} />
    </MainTemplate>
  )
}