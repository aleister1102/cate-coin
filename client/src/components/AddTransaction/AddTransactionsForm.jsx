import React, { useState } from 'react'
import ToastMessage from '../ToastMessage'
import { Button } from './Button'
import { ControlGroup } from './ControlGroup'

export const TransactionContext = React.createContext()

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
					<TransactionContext.Provider
						key={index}
						value={{
							transaction,
							index,
							handleInputChange,
							handleRemoveTransaction,
						}}>
						<ControlGroup />
					</TransactionContext.Provider>
				))}

				<div className='flex justify-around w-full'>
					<Button
						text={'Add transaction'}
						handler={handleAddTransaction}
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
