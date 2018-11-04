import React from 'react'
import nanoid from 'nanoid'
import { BalanceSheet } from '../components/ChatElements/RichContent/BalanceSheet'
import { BranchLocation } from '../components/ChatElements/RichContent/BranchLocation'
import { WithdrawalHistory } from '../components/ChatElements/RichContent/WithdrawalHistory'

export interface BotResponse {
	message: string,
	rich_content?: RichContent
}

export interface RichContent {
	arguments: any,
	card_type: 'balance-sheet' | 'closest-branch' | 'withdrawal-history' | 'deposit-history' | 'purchase-history' | string
}

export function richContentResolver (content: RichContent): JSX.Element | null {
	switch (content.card_type) {
		case 'balance-sheet':
			return <BalanceSheet key={nanoid()} data={content.arguments}/>
		case 'closest-branch':
			return <BranchLocation key={nanoid()} {...content.arguments}/>
		case 'withdrawal-history':
		case 'deposit-history':
		case 'purchase-history':
			return <WithdrawalHistory key={nanoid()} {...content.arguments}/>

		default:
			return null
	}
}
