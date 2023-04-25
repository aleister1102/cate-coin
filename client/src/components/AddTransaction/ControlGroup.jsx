import React, { useContext } from 'react'
import { Input } from './Input'
import { Button } from './Button'
import { TransactionContext } from './AddTransactionsForm'

export function ControlGroup() {
	const { transaction, index, handleRemoveTransaction } =
		useContext(TransactionContext)
	const isRemovable = index > 0

	return (
		<div className='control-group flex flex-col w-full items-center mt-4 border border-primary rounded-xl p-4'>
			<h3 className='font-bold'>Transaction {index + 1}</h3>

			{Object.keys(transaction).map((name) => (
				<Input
					key={`${index}-${name}`}
					name={name}
					type={
						name === 'amount' || name === 'change'
							? 'number'
							: 'text'
					}
				/>
			))}

			{isRemovable && (
				<Button
					text='Remove transaction'
					handler={handleRemoveTransaction}
				/>
			)}
		</div>
	)
}
