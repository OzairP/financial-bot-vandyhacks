import * as React from 'react'
import './BalanceSheet.scss'

export interface BalanceSheetProps {
	data: Array<{
		account_name: string,
		balance: number
	}>
}

export class BalanceSheet extends React.Component<BalanceSheetProps> {

	public render () {
		return (
			<div className='cb-rich-balance-sheet'>
				{
					this.props.data
						.map((d, i) =>
							<div key={i} className='cb-rich-balance-sheet__account'>
								<span>{d.account_name}</span>
								<span>${(Math.round(d.balance * 100) / 100).toLocaleString('en', {useGrouping:true})}</span>
							</div>
						)
				}
			</div>
		)
	}

}
