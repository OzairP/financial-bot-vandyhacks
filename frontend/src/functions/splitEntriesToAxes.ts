export function splitEntriesToAxes (d: Array<[any, any]>) {
	const x = []
	const y = []

	for (let i = 0; i < d.length; i++) {
		x[i] = d[i][0]
		y[i] = d[i][1]
	}

	return [x,y]
}
