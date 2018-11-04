import * as React from 'react'
import { mergeLikeKeys } from '../../../functions/mergeLikeKeys'
import { BezierPlot } from '../../BezierPlot'
import { splitEntriesToAxes } from '../../../functions/splitEntriesToAxes'
import './WithdrawalHistory.scss'

export interface WithdrawalHistoryProps {
	payer_id: string,
	data: {
		amount: Array<number>,
		transaction_date: Array<string>
		purchase_date: Array<string>
	}
}

interface WithdrawalHistoryState {
	x: Array<number>,
	y: Array<number>
}


export class WithdrawalHistory extends React.Component<WithdrawalHistoryProps, WithdrawalHistoryState> {

	public state = {
		x: [],
		y: [],
	}

	protected graph: React.RefObject<HTMLDivElement> = React.createRef()

	public componentDidMount () {
		let [x, y] = splitEntriesToAxes(Object.entries(mergeLikeKeys(this.props.data.transaction_date || this.props.data.purchase_date, this.props.data.amount)))
		x = x.map((_, i) => i).slice(0, 14)
		y = y.slice(0, 14)
		this.setState({x, y})
	}

	public render () {
		return (
			<div ref={this.graph} className="cb-withdrawal-graph">
				<BezierPlot x={this.state.x} y={this.state.y} width="360px" height="203px" />
			</div>
		)
	}

}
