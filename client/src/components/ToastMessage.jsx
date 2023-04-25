import { useEffect, useState } from 'react'

export default function ToastMessage({ message, duration = 3000, onClose}) {
	const [isOpen, setIsOpen] = useState(false)

	useEffect(() => {
		setIsOpen(true)

		const timeoutId = setTimeout(() => {
			setIsOpen(false)
		}, duration)

		return () => {
			clearTimeout(timeoutId)
		}
	}, [duration, onClose])

	return (
		<div
			className={`${
				isOpen ? 'opacity-100' : 'opacity-0'
			} transition-opacity duration-300 fixed top-4 right-4 z-50`}>
			<div className='bg-violet-500 text-white p-4 px-4 rounded-lg'>
				{message}
			</div>
		</div>
	)
}
