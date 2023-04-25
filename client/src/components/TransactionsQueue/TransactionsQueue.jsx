import React, { useState, useEffect } from 'react'
import { parseTransactionString } from '../../utils/utils'

export default function TransactionsQueue({ blockchain }) {
	const [transactionStrings, setTransactionStrings] = useState([])

	useEffect(() => {
		setTransactionStrings(blockchain.transactions_queue)
	}, [blockchain])

	const transactions = transactionStrings
		? transactionStrings.map((transaction) =>
				parseTransactionString(transaction),
		  )
		: []

	return (
		<table className='w-3/4 mt-44 mx-auto shadow-md border overflow-hidden rounded-2xl'>
			<thead>
				<tr className='bg-primary'>
					<th>ID</th>
					<th>Sender</th>
					<th>Receiver</th>
					<th>Amount</th>
					<th>Change</th>
				</tr>
			</thead>
			<tbody>
				{transactions.map((transaction, index) => (
					<tr
						key={index}
						className=''>
						<td>{index + 1}</td>
						<td>{transaction.sender}</td>
						<td>{transaction.receiver}</td>
						<td>{transaction.amount}</td>
						<td>{transaction.change}</td>
					</tr>
				))}
			</tbody>
		</table>
	)
}
