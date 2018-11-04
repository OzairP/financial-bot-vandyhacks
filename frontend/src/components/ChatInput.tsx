import * as React from 'react'
import { RefObject } from 'react'
import './ChatInput.scss'
import { DictationProcessor } from './DictationProcessor'
import Transition from 'react-transition-group/Transition'

interface ChatInputState {
	input: string,
	inputPlaceholder: string,
	dictating: boolean,
}

export interface ChatInputProps {
	onInput: (input: string) => void
	disabled?: boolean
}

export class ChatInput extends React.Component<ChatInputProps, ChatInputState> {

	public state = {
		input: '',
		inputPlaceholder: 'Start typing...',
		dictating: false
	}

	protected input: RefObject<HTMLInputElement> = React.createRef()

	public render () {
		const {
			input,
			inputPlaceholder,
			dictating,
		} = this.state

		return (
			<div className="cb-chat-input">

				<Transition
					in={dictating}
					timeout={300}
					mountOnEnter
					unmountOnExit
				>{animationStatus =>
					<div className={`cb-chat-input__dictation cb-chat-input__dictation--${animationStatus}`}>
						<DictationProcessor
							onStart={this.onRecognitionStart.bind(this)}
							onInput={this.onRecognitionResult.bind(this)}
							onEnd={this.onRecognitionStop.bind(this)}
							onError={this.onRecognitionError.bind(this)}
						/>
					</div>
				}</Transition>

				<input
					className="cb-chat-input__type"
					placeholder={inputPlaceholder}
					disabled={dictating || this.props.disabled}
					ref={this.input}
					onChange={this.onTyping.bind(this)}
					onKeyUp={this.onKeyDown.bind(this)}
				/>

				<div className="cb-chat-input__transition-pair">
					<button
						className={`cb-chat-input__action ${input.length === 0 || dictating ? '' : 'exited'} ${dictating ? 'cb-chat-input__action--flash' : ''}`}
						onClick={this.onDictate.bind(this)}>
						<svg style={{width: '24px', height: '24px'}} viewBox="0 0 24 24">
							<path
								d="M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z" />
						</svg>
					</button>
					<button className={`cb-chat-input__action ${input.length > 0 && !dictating ? '' : 'exited'}`}
							onClick={this.onSubmit.bind(this)}>
						<svg style={{width: '24px', height: '24px'}} viewBox="0 0 24 24">
							<path fill="#000000" d="M2,21L23,12L2,3V10L17,12L2,14V21Z" />
						</svg>
					</button>
				</div>
			</div>
		)
	}

	private onKeyDown (event: React.KeyboardEvent<HTMLInputElement>) {
		if (event.keyCode !== 13) {
			return
		}

		this.onSubmit()
	}

	protected onTyping (event: React.ChangeEvent<HTMLInputElement>) {
		const {value: input} = event.currentTarget

		this.setState({input})
	}

	protected onSubmit () {
		if (this.props.disabled) {
			return
		}

		this.props.onInput(this.state.input)
		this.setState({
			input: ''
		}, () => this.input.current!.value = '')
	}

	protected onDictate () {
		if (this.props.disabled) {
			return
		}

		if (this.state.dictating) {
			this.setState({
				inputPlaceholder: 'Start typing...',
				dictating: false,
			})
		} else {
			if (this.state.input !== '') {
				return
			}

			this.setState(({dictating}) => ({
				inputPlaceholder: 'Starting speech recognition...',
				dictating: !dictating
			}))
		}
	}

	protected onRecognitionStart () {
		this.setState({
			inputPlaceholder: 'Start speaking...'
		})
	}

	protected onRecognitionStop () {
		this.setState({
			inputPlaceholder: 'Start typing...',
			dictating: false,
		})
	}

	protected onRecognitionError (e: Error | SpeechRecognitionError) {
		if ('error' in e) {
			if (e.error === 'aborted') {
				return
			}
			if (e.error === 'no-speech') {
				this.setState({
					inputPlaceholder: 'No speech is being detected...',
				})
				return
			}
		}

		console.error(e)
		alert(e.message)
		this.setState({
			inputPlaceholder: 'Start typing...',
			dictating: false,
		})
	}

	protected onRecognitionResult (result: string) {
		this.setState(s => ({
			input: s.input + result
		}), () => this.input.current!.value = this.state.input)
	}
}
