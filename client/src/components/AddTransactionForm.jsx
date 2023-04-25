import React, { useState } from 'react'
import { capitalizeString } from '../utils/utils'
import ToastMessage from './ToastMessage'

const controls = [
	{
		name: 'sender',
		type: 'text',
	},
	{
		name: 'receiver',
		type: 'text',
	},
	{
		name: 'amount',
		type: 'number',
	},
	{
		name: 'change',
		type: 'number',
	},
]

const initialFormData = {
	sender: '',
	receiver: '',
	amount: 1,
	change: 0,
}

export default function AddTransactionForm() {
	const [formData, setFormData] = useState(initialFormData)
	const [toastMessage, setToastMessage] = useState('')
	const [showToast, setShowToast] = useState(false)

	const handleInputChange = (event) => {
		const { name, value } = event.target
		setFormData({ ...formData, [name]: value })
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
					body: JSON.stringify({ transactions: [formData] }),
				},
			)

			const data = await response.json()

			if (data) {
				setToastMessage(data.message)
				setShowToast(true)
				setFormData(initialFormData)
			}
		} catch (error) {
			console.error('Error:', error)
			setToastMessage('An error occurred while adding the transaction 😔')
			setShowToast(true)
		}
	}

	return (
		<div className='flex justify-center items-center m-auto'>
			<form
				onSubmit={handleSubmit}
				className='mt-44 p-4 rounded-xl shadow-md shadow-gray-300 w-1/3 flex flex-col items-center'>
				{controls.map(({ name, type }, index) => (
					<div
						key={index}
						className='flex flex-col w-full'>
						<label htmlFor={name}>{capitalizeString(name)}</label>
						<input
							name={name}
							type={type}
							min={name === 'amount' ? 1 : 0}
							value={formData[name]}
							onChange={handleInputChange}
							required
							className='outline-none border border-primary rounded-xl text-base p-2'
						/>
					</div>
				))}
				<button className='bg-primary rounded-xl p-3 hover:bg-pink-600 text-white mt-4'>
					Add transaction
				</button>
			</form>
			{showToast && (
				<ToastMessage
					message={toastMessage}
					onClose={() => setShowToast(false)}
				/>
			)}
		</div>
	)
}
