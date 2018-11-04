import React from 'react'
import { ChatMessage, ChatMessageProps } from './ChatMessage'
import './TypingIndicator.scss'

interface TypingIndicatorProps {
	side: ChatMessageProps['side']
}

export function TypingIndicator (props: TypingIndicatorProps) {
	return (
		<ChatMessage side={props.side}>
			<div className="cb-typing-indicator">
				<div className="cb-typing-indicator__ball" />
				<div className="cb-typing-indicator__ball" />
				<div className="cb-typing-indicator__ball" />
			</div>
		</ChatMessage>
	)
}
