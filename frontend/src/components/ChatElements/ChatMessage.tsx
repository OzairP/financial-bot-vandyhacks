import * as React from 'react'
import './ChatMessage.scss'

export interface ChatMessageProps {
	side: 'left' | 'right'
	children: string | JSX.Element
}

export function ChatMessage (props: ChatMessageProps) {
	const {
		side,
		children,
	} = props

	return (
		<div className={`cb-chat-message cb-chat-message--${side}`}>
			<span>{children}</span>
		</div>
	)
}
