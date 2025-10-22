<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Skeleton } from '$lib/components/ui/skeleton';
</script>

<div class="space-y-3">
	<Card.Root>
		<Card.Header>
			<Skeleton class="h-6 w-3/4" />
			<Skeleton class="h-4 w-1/4" />
		</Card.Header>
	</Card.Root>
	<Card.Root>
		<Card.Header>
			<Skeleton class="h-6 w-3/4" />
			<Skeleton class="h-4 w-1/4" />
		</Card.Header>
	</Card.Root>
	<Card.Root>
		<Card.Header>
			<Skeleton class="h-6 w-3/4" />
			<Skeleton class="h-4 w-1/4" />
		</Card.Header>
	</Card.Root>
</div>
