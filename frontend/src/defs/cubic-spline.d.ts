declare module 'cubic-spline' {
	function spline(x: number, x_sample: Array<number>, y_sample: Array<number>): number

	export = spline
}
