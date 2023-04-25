import React, { useState } from 'react'
import ToastMessage from '../ToastMessage'
import Block from '../Blockchain/Block'
import { MiningGIF } from './MiningGIF'

export default function MineBlock() {
	const initialToastMessage = {
		message: '',
		show: false,
	}
	const [isMining, setIsMining] = useState(false)
	const [toastMessage, setToastMessage] = useState(initialToastMessage)
	const [newBlock, setNewBlock] = useState(null)

	const handleClick = async (event) => {
		event.preventDefault()

		setIsMining(true)
		setToastMessage(initialToastMessage)
        setNewBlock(null)

		try {
			const response = await fetch('http://localhost:8080/mine-block')
			const status = response.status
			const data = await response.json()

			if (data) {
				setToastMessage({ message: data.message, show: true })
				setIsMining(false)

				if (status === 200) {
					setNewBlock(data.block)
				}
			}
		} catch (error) {
			console.log(error)
		}
	}

	return (
		<div className='mt-32 m-auto flex flex-col justify-center items-center'>
			<button
				onClick={handleClick}
				type='button'
				className='bg-primary rounded-xl p-4 hover:bg-pink-600 text-white mt-4 text-xl uppercase font-bold mb-8'>
				Mine new block
			</button>
			{isMining ? <MiningGIF /> : null}
			{toastMessage.show && (
				<ToastMessage
					message={toastMessage.message}
					onClose={() => setShowToast(false)}
				/>
			)}
			{newBlock ? <Block block={newBlock} /> : null}
		</div>
	)
}
