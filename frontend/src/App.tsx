import React, { useState } from 'react'
import './App.scss'
import { ChatHistory } from './components/ChatHistory'
import { ChatInput } from './components/ChatInput'
import { ChatMessage } from './components/ChatElements/ChatMessage'
import { TypingIndicator } from './components/ChatElements/TypingIndicator'

function App () {
	const [message, setMessage] = useState('')

	setTimeout(() => {
		setMessage('Foo bar')
	}, 5000)

	return (
		<div className="App">
			<div className="cb-io">
				<ChatHistory>
					<ChatMessage side="right">Hello</ChatMessage>
					<ChatMessage side="left">World</ChatMessage>
					<ChatMessage
						side="left">jwio2j3i2jr3jr23r23jr23r23r23rjwio2j3i2jr3jr23r23jr23r23r23rjwio2j3i2jr3jr23r23jr23r23r23rjwio2j3i2jr3jr23r23jr23r23r23r</ChatMessage>
					<TypingIndicator side="left" message={message} />
				</ChatHistory>
				<ChatInput />
			</div>
		</div>
	)
}

export default App
