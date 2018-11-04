import React from 'react'
import './ChatHistory.scss'

export function ChatHistory (props: React.Props<{}>) {
	return (
		<div className='cb-chat-history'>
			{props.children}
		</div>
	)
}
