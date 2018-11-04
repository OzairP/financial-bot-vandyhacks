import * as React from 'react'
import { COLORS } from '../global'

export interface BezierPlotProps {
	x: Array<number>,
	y: Array<number>,
	width: string,
	height: string,
	stroke?: string,
	fill?: string,
}

export class BezierPlot extends React.Component<BezierPlotProps> {

	protected canvas: React.RefObject<HTMLCanvasElement> = React.createRef()

	protected ctx: CanvasRenderingContext2D | null = null

	public componentDidMount () {
		if (!this.canvas.current) {
			return
		}

		const canvas = this.canvas.current
		this.ctx = canvas.getContext('2d')!

		const h = canvas.height
		const w = canvas.width
		canvas.height = h * 2
		canvas.width = w * 2
		canvas.style.height = `${h}px`
		canvas.style.width = `${w}px`
		this.ctx.scale(2, 2)

		window.requestAnimationFrame(this.draw.bind(this))
	}

	public render () {
		return (
			<canvas ref={this.canvas} width={this.props.width} height={this.props.height} />
		)
	}

	protected getCurve (width: number, x_set: Array<number>, y_set: Array<number>) {
		const fn = (x: number) => y_set[x]

		const output: Array<[number, number]> = []

		for (let i = 0; i < x_set.length; i++) {
			output[i] = [
				width * ((x_set.length - (x_set.length - i)) / x_set.length),
				fn(i) - this.canvas.current!.height / 4
			]
		}

		const y_max = Math.max(...output.map(([, y]) => y))
		const y_scale = this.canvas.current!.height / (y_max * 2)

		const x_max = Math.max(...output.map(([x]) => x))
		const x_scale = width / (x_max * 2)

		return output.map(([x, y]) => [x * x_scale, y * y_scale])
	}

	protected draw () {
		if (!this.ctx || !this.canvas.current) {
			return
		}

		const canvas = this.canvas.current
		const ctx = this.ctx

		ctx.clearRect(0, 0, canvas.width, canvas.height)
		ctx.beginPath()
		ctx.lineWidth = 2
		ctx.fillStyle = this.props.stroke || COLORS['blue-dark']
		ctx.strokeStyle = this.props.stroke || COLORS['blue-light']

		const curve = this.getCurve(canvas.width, this.props.x, this.props.y)

		ctx.moveTo(curve[0][0], curve[0][1])

		for (let i = 1; i < curve.length - 2; i++) {
			const xc = (curve[i][0] + curve[i + 1][0]) / 2
			const yc = (curve[i][1] + curve[i + 1][1]) / 2
			ctx.quadraticCurveTo(curve[i][0], curve[i][1], xc, yc)
		}
		// curve through the last two points
		ctx.quadraticCurveTo(curve[curve.length - 2][0], curve[curve.length - 2][1], curve[curve.length - 1][0], curve[curve.length - 1][1])

		ctx.stroke()

		ctx.lineTo(curve[curve.length - 1][0], canvas.height)
		ctx.lineTo(curve[0][0], canvas.height)
		ctx.fill()
	}

}
