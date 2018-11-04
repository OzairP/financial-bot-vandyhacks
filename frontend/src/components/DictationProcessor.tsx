import React from 'react'
import './DictationProcessor.scss'
import { COLORS } from '../global'

interface RefObject<T> {
	readonly current: T | null;
}

interface DictationProcessorProps {
	onStart: () => void
	onInput: (text: string) => void
	onEnd: () => void,
	onError: (error: SpeechRecognitionError | Error) => void
}

export class DictationProcessor extends React.Component<DictationProcessorProps> {

	protected mediaStream: MediaStreamAudioSourceNode | null = null

	protected canvas: RefObject<HTMLCanvasElement> = React.createRef()

	protected canvasCtx: CanvasRenderingContext2D | null = null

	protected t_0: number = new Date().getTime()

	protected lastAmplitude: number | boolean = false

	protected speechRecognition: SpeechRecognition | null = null

	public async componentDidMount () {
		const SpeechRecognition_: typeof SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition

		if (!SpeechRecognition_) {
			this.props.onError(Error('This browser does not speech recognition'))
			return
		}

		this.speechRecognition = new SpeechRecognition_()

		this.speechRecognition.continuous = true

		this.speechRecognition.onaudiostart = () => {
			this.lastAmplitude = 0
			this.props.onStart()
		}
		this.speechRecognition.onaudioend = () => {
			this.lastAmplitude = false
			this.props.onEnd()
		}
		this.speechRecognition.onerror = this.props.onError
		this.speechRecognition.onresult = (event) => {
			console.log(event)
			const current = event.resultIndex
			const transcript = event.results[current][0].transcript

			// Fixes double transcription on Android
			if (current !== 1 || transcript !== event.results[0][0].transcript) {
				this.props.onInput(transcript)
				console.log(transcript)
			}
		}

		this.speechRecognition.start()

		const audioCtx = new AudioContext()

		this.mediaStream = audioCtx.createMediaStreamSource(
			await navigator.mediaDevices.getUserMedia({audio: true})
		)

		const levelsProcessor = audioCtx.createScriptProcessor(1024, 1, 1)

		this.mediaStream.connect(levelsProcessor)
		levelsProcessor.connect(audioCtx.destination)

		levelsProcessor.onaudioprocess = event => {
			if (this.lastAmplitude === false) {
				return
			}

			const buf = event.inputBuffer.getChannelData(0)
			const len = buf.length
			let rms = 0

			// Iterate through buffer
			for (let i = 0; i < len; i++) {
				rms += Math.abs(buf[i])
			}
			rms = Math.sqrt(rms / len)

			this.lastAmplitude = rms
		}

		this.canvasCtx = this.canvas.current!.getContext('2d')

		if (this.canvas.current) {
			const canvas = this.canvas.current
			const h = canvas.height
			const w = canvas.width
			canvas.height = h * 2
			canvas.width = w * 2
			canvas.style.height = `${h}px`
			canvas.style.width = `${w}px`
			this.canvasCtx!.scale(2, 2)
		}

		window.requestAnimationFrame(this.draw.bind(this))
	}

	public componentWillUnmount () {
		this.mediaStream && this.mediaStream.mediaStream.getTracks()[0].stop()
		this.speechRecognition && this.speechRecognition.abort()
	}

	public render () {
		return (
			<div className="cb-dictation-processor">
				<canvas
					ref={this.canvas}
					className="cb-dictation-processor__canvas"
					width="400px"
				/>
			</div>
		)
	}

	protected getSinusoidPath (canvasWidth: number, amplitude: number, frequency: number = 0.25, phaseShift: number = 0) {
		const output: Array<[number, number]> = []
		const midPoint = canvasWidth / 4

		const fn = (x: number) =>
			amplitude * ((midPoint - Math.abs(midPoint - x)) / (midPoint)) *
			Math.sin(x * frequency + phaseShift) + 85

		for (let i = 0; i < canvasWidth; i++) {
			output[i] = [i, fn(i)]
		}
		return output
	}

	protected draw () {
		if (!this.canvasCtx || !this.canvas.current) {
			return
		}

		const canvas = this.canvas.current
		const ctx = this.canvasCtx
		const runtime = new Date().getTime() - this.t_0
		const sinusoids = 5
		const amplitude = typeof this.lastAmplitude === 'boolean' ? 0 : this.lastAmplitude

		ctx.clearRect(0, 0, canvas.width, canvas.height)

		for (let s = 0; s < sinusoids; s++) {
			const scaleFactor = (s + 1) / sinusoids
			ctx.beginPath()
			ctx.lineWidth = 1
			ctx.strokeStyle = ((x) => {
				return x === 0 ? COLORS['blue'] : x === 1 ? COLORS['blue-dark'] : COLORS['blue-light']
			})(s % 3)

			const pointList = this.getSinusoidPath(
				canvas.width,
				amplitude * scaleFactor * 100,
				0.02,
				360 * scaleFactor + (runtime / 50 % 360 * scaleFactor)
			)

			for (let i = 0; i < pointList.length; i++) {
				if (i === 0) {
					ctx.moveTo(pointList[0][0], pointList[0][1])
				} else {
					ctx.lineTo(pointList[i][0], pointList[i][1])
				}
			}
			ctx.stroke()
		}

		window.requestAnimationFrame(this.draw.bind(this))
	}

}
