import type { PageLoad } from "./$types"
import { getVisits } from "./queryFn"

export const load: PageLoad = async ({ parent, fetch }) => {
  const { queryClient } = await parent()

  await queryClient.prefetchQuery({
    queryKey: ['questions'],
    queryFn: () => getVisits(fetch),
  })

}
