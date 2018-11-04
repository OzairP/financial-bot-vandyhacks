import React, { Component, RefObject } from 'react'
import './ChatHistory.scss'
import { TypingIndicator } from './ChatElements/TypingIndicator'
import Transition from 'react-transition-group/Transition'

export interface ChatHistoryProps {
	leftTyping?: boolean,
}

interface ChatHistoryState {
	heightOffset: number,
	messages: number
}

export class ChatHistory extends Component<ChatHistoryProps, ChatHistoryState> {

	public transcript: RefObject<HTMLDivElement> = React.createRef()

	public state = {
		heightOffset: 0,
		messages: 0,
	}

	public componentDidMount () {
		this.transcript.current!.style.transform = `translateY(-${this.getMessagesHeight()}px)`
	}

	public componentDidUpdate (prevProps: Readonly<ChatHistoryProps>, prevState: Readonly<ChatHistoryState>) {
		if (this.transcript.current) {
			setTimeout(() => {
				if (this.transcript.current) {
					this.transcript.current.style.transform = `translateY(-${this.getMessagesHeight()}px)`
				}
			}, 300)

			if (this.state.messages !== this.getMessageTotal()) {
				this.setState({
					messages: this.getMessageTotal()
				})
			}
		}
	}

	public render () {
		return (
			<div className="cb-chat-history">
				<Transition timeout={300} in={this.state.messages === 0}>{state =>
					<div className={`cb-chat-history__initial cb-chat-history__initial--${state}`}>
						<h1>Good {
							new Date().getHours() < 12 ? 'morning' :
								new Date().getHours() < 18 ? 'afternoon' : 'night'
						} Ozair, what can I help you with?
						</h1>
						<h2>Some things you can ask me:</h2>
						<div className="cb-chat-history__example">
							<svg viewBox="0 0 24 24">
								<path
									d="M20,18H4V6H20M20,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V6C22,4.89 21.1,4 20,4M11,17H13V16H14A1,1 0 0,0 15,15V12A1,1 0 0,0 14,11H11V10H15V8H13V7H11V8H10A1,1 0 0,0 9,9V12A1,1 0 0,0 10,13H13V14H9V16H11V17Z" />
							</svg>
							<div className="cb-chat-history__detail">
								<h3>Status</h3>
								<p>"What's my balance?"</p>
							</div>
						</div>
						<div className="cb-chat-history__example">
							<svg viewBox="0 0 24 24">
								<path
									d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z" />
							</svg>
							<div className="cb-chat-history__detail">
								<h3>Locate something</h3>
								<p>"Where is the nearest branch?"</p>
							</div>
						</div>
						<div className="cb-chat-history__example">
							<svg viewBox="0 0 24 24">
								<svg viewBox="0 0 24 24">
									<path
										d="M15,14V11H18V9L22,12.5L18,16V14H15M14,7.7V9H2V7.7L8,4L14,7.7M7,10H9V15H7V10M3,10H5V15H3V10M13,10V12.5L11,14.3V10H13M9.1,16L8.5,16.5L10.2,18H2V16H9.1M17,15V18H14V20L10,16.5L14,13V15H17Z" />
								</svg>
							</svg>
							<div className="cb-chat-history__detail">
								<h3>Transfer money</h3>
								<p>"I want to make a transfer."</p>
							</div>
						</div>
						<div className="cb-chat-history__example">
							<svg viewBox="0 0 24 24">
								<svg viewBox="0 0 24 24">
									<path d="M3,22V8H7V22H3M10,22V2H14V22H10M17,22V14H21V22H17Z" />
								</svg>
							</svg>
							<div className="cb-chat-history__detail">
								<h3>Track your history</h3>
								<p>"Show my purchase history."</p>
							</div>
						</div>
					</div>
				}</Transition>
				<div
					className="cb-chat-history__transcript"
					ref={this.transcript}
				>
					{this.props.children}
				</div>
				<Transition
					timeout={300}
					in={this.props.leftTyping}
				>{state =>
					<div className={`cb-chat-history__indicators cb-chat-history__indicators--${state}`}>
						<TypingIndicator side="left" />
					</div>
				}</Transition>

			</div>
		)
	}

	public getMessagesHeight () {
		if (!this.transcript.current) {
			return 0
		}

		return Array.from(this.transcript.current.children)
			.reduce((sum, el) => sum + el.clientHeight + 25, 0) + (this.props.leftTyping ? 62 : 0)
	}

	public getMessageTotal () {
		if (!this.transcript.current) {
			return 0
		}

		return this.transcript.current.children.length
	}
}
