import * as React from 'react'
import './ChatMessage.scss'

export interface ChatMessageProps {
	side: 'left' | 'right'
	children: string | JSX.Element
	className?: string
}

export function ChatMessage (props: ChatMessageProps) {
	const {
		side,
		children,
		className,
	} = props
	return (
		<div className={`cb-chat-message cb-chat-message--${side} ${className || ''}`}>
			{children}
		</div>
	)
}
