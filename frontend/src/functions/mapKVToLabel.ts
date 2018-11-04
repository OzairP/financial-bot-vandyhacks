export function mapKVToLabel (l1: string, l2: string, d: Record<string, number>) {
	return Object.entries(d).map(([k,v]) => ({
		[l1]: k,
		[l2]: v
	}))
}
