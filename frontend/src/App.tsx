import React, { Component } from 'react'
import './App.scss'
import { ChatHistory } from './components/ChatHistory'
import { ChatInput } from './components/ChatInput'
import { ChatMessage } from './components/ChatElements/ChatMessage'
import axios from 'axios'
import { CONSTANTS } from './CONSTANTS'
import { BotResponse, richContentResolver } from './functions/richContentResolver'
import { promiseDelay } from './functions/promiseDelay'
import { sleep } from './functions/sleep'
import { WithdrawalHistory } from './components/ChatElements/RichContent/WithdrawalHistory'

(window as any).axios = axios

interface AppState {
	messages: Array<JSX.Element>
	botTyping: boolean
}

class App extends Component<{}, AppState> {

	public state = {
		messages: [],
		botTyping: false,
	}

	public render () {
		return (
			<div className="App">
				<div className="cb-io">
					<ChatHistory leftTyping={this.state.botTyping}>
						{this.state.messages}
					</ChatHistory>
					<ChatInput onInput={this.onInput.bind(this)} disabled={this.state.botTyping} />
				</div>
			</div>
		)
	}

	/**
	 * @param {string} message
	 */
	protected async onInput (message: string) {
		this.setState(s => ({
			messages: s.messages.concat(<ChatMessage key={s.messages.length} side="right">{message}</ChatMessage>),
		}))

		await sleep(500)

		this.setState({ botTyping: true })

		const response = await promiseDelay(axios.post<BotResponse>('/queries', {
			user_id: CONSTANTS.user_id,
			query: message
		}), 1000)

		const richContent = response.data.rich_content ? richContentResolver(response.data.rich_content) : undefined

		this.setState({ botTyping: false }, async () => {
			await sleep(500)
			this.setState(s => ({
				messages:
					s.messages.concat(
						<ChatMessage key={s.messages.length} side="left">{response.data.message}</ChatMessage>,
						richContent!
					).filter(e => !!e)
			}))
		})
	}
}

export default App
