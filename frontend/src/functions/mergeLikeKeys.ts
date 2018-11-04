export function mergeLikeKeys (d1: Array<string>, d2: Array<number>) {
	const results: Record<string, number> = {}
	for (let i = 0; i < d1.length; i++) {
		const key = d1[i]
		const value = d2[i]
		key in results ? results[key] = results[key] + value : results[key] = value
	}
	return results
}
