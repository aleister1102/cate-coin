import React from 'react'

export function Button({ text, handler }) {
	return (
		<button
			className='btn'
			type={handler ? 'button' : 'submit'}
			onClick={handler}>
			{text}
		</button>
	)
}
