import React from 'react'
import './BranchLocation.scss'
import { CONSTANTS } from '../../../CONSTANTS'

export interface BranchLocationProps {
	address: string,
	branch_name: string,
	distance: number,
	hours: string,
	notes: Array<string>,
	phone_number: string
}

export class BranchLocation extends React.Component<BranchLocationProps> {

	public render () {
		return (
			<div className="cb-branch">
				<div className="cb-branch__map">
					<iframe
						src={`https://www.google.com/maps/embed/v1/place?key=${CONSTANTS.gkey}&q=${this.props.address}`}
						height='353px'
						width='150px'
						frameBorder="0" scrolling="no"
					/>
				</div>
				<div className="cb-branch__data">
					<p className="cb-branch__name">{this.props.branch_name}</p>
					<p className="cb-branch__address">
						<a href={`https://www.google.com/maps/dir/?key=${CONSTANTS.gkey}&api=1&destination=${this.props.address}`}>
							{this.props.address}
						</a>
					</p>
					<p className="cb-branch__phone">
						<a href={`tel:${this.props.phone_number}`}>
							{this.props.phone_number}
						</a>
					</p>
					<p className="cb-branch__features">
						{this.props.notes.join(' · ')}
					</p>
				</div>
			</div>
		)
	}

}
