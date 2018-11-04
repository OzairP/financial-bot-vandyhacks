export function csvTransformer (titles: Array<string>, data: Object) {
	return titles.join(',') + '\n' + Object.entries(data).reduce((acc, str) => `${acc}${str[0]},${str[1]}\n`, '')
}
