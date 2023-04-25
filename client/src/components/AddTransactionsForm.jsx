import React, { useState } from 'react'
import { capitalizeString } from '../utils/utils'
import ToastMessage from './ToastMessage'

function Input({ name, type, transaction, index, handleInputChange }) {
	return (
		<div
			key={name}
			className='flex flex-col w-full'>
			<label htmlFor={name}>{capitalizeString(name)}</label>
			<input
				name={name}
				type={type}
				min={name == 'amount' ? 1 : 0}
				value={transaction[name]}
				pattern={
					name == 'sender' || name == 'receiver'
						? '[a-zA-Z]{1,10}'
						: null
				}
				title={
					name == 'sender' || name == 'receiver'
						? 'Only letters and max 10 characters'
						: null
				}
				onChange={(event) => handleInputChange(event, index)}
				required
				className='outline-none border border-primary rounded-xl text-base p-2'
			/>
		</div>
	)
}

function Inputs({ transaction, index, handleInputChange }) {
	return Object.keys(transaction).map((name) => (
		<Input
			index={index}
			name={name}
			type={name == 'amount' || name == 'change' ? 'number' : 'text'}
			transaction={transaction}
			handleInputChange={handleInputChange}
			key={`{index}-${name}`}
		/>
	))
}

function Button({ handler, index, text }) {
	return (
		<button
			className='btn'
			type={handler ? 'button' : 'submit'}
			onClick={() => {
				handler ? handler(index) : null
			}}>
			{text}
		</button>
	)
}

function ControlGroup({
	transaction,
	index,
	handleInputChange,
	handleRemoveTransaction,
}) {
	return (
		<div className='control-group flex flex-col w-full items-center mt-4 border border-primary rounded-xl p-4'>
			<h3>Transaction {index + 1}</h3>

			<Inputs
				transaction={transaction}
				index={index}
				handleInputChange={handleInputChange}
			/>

			{index > 0 && (
				<Button
					handler={handleRemoveTransaction}
					index={index}
					text={'Remove transaction'}
					className={'w-full'}
				/>
			)}
		</div>
	)
}

export default function AddTransactionsForm() {
	const initialTransaction = {
		sender: '',
		receiver: '',
		amount: 1,
		change: 0,
	}

	const initialToastMessage = {
		message: '',
		show: false,
	}

	const [transactions, setTransactions] = useState([initialTransaction])
	const [toastMessage, setToastMessage] = useState(initialToastMessage)

	const handleInputChange = (event, index) => {
		const { name, value } = event.target
		const newTransactions = [...transactions]
		newTransactions[index][name] = value
		setTransactions(newTransactions)
	}

	const handleAddTransaction = () => {
		setTransactions([...transactions, initialTransaction])
	}

	const handleRemoveTransaction = (index) => {
		const newTransactions = [...transactions]
		newTransactions.splice(index, 1)
		setTransactions(newTransactions)
	}

	const handleSubmit = async (event) => {
		event.preventDefault()

		try {
			const response = await fetch(
				'http://localhost:8080/add-transactions',
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ transactions }),
				},
			)

			const data = await response.json()

			if (data) {
				setToastMessage({ message: data.message, show: true })
				setTransactions([initialTransaction])
			}
		} catch (error) {
			console.error('Error:', error)
		}
	}

	return (
		<div className='flex justify-center items-center m-auto'>
			<form
				onSubmit={handleSubmit}
				className='mt-44 mb-24 p-4 rounded-xl shadow shadow-slate-400 w-1/3 flex flex-col items-center'>
				{transactions.map((transaction, index) => (
					<ControlGroup
						key={index}
						transaction={transaction}
						index={index}
						handleInputChange={handleInputChange}
						handleRemoveTransaction={handleRemoveTransaction}
					/>
				))}

				<div className='flex justify-around w-full'>
					<Button
						handler={handleAddTransaction}
						text={'Add transaction'}
					/>
					<Button text={'Submit'} />
				</div>
			</form>

			{toastMessage.show && (
				<ToastMessage
					message={toastMessage.message}
					onClose={() => setShowToast(false)}
				/>
			)}
		</div>
	)
}
