import React, { useContext } from 'react'
import { capitalizeString } from '../../utils/utils'
import { TransactionContext } from './AddTransactionsForm'

export function Input({ name, type }) {
	const { transaction, index, handleInputChange } =
		useContext(TransactionContext)

	const min = name === 'amount' ? 1 : 0
	const pattern =
		name === 'sender' || name === 'receiver' ? '[a-zA-Z]{1,10}' : null
	const title =
		name === 'sender' || name === 'receiver'
			? 'Only letters and max 10 characters'
			: null

	return (
		<div
			key={name}
			className='flex flex-col w-full'>
			<label htmlFor={name}>{capitalizeString(name)}</label>
			<input
				name={name}
				type={type}
				min={min}
				value={transaction[name]}
				pattern={pattern}
				title={title}
				onChange={(event) => handleInputChange(event, index)}
				required
				className='outline-none border border-primary rounded-xl text-base p-2'
			/>
		</div>
	)
}