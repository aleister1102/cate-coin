import React from 'react'

const capitalizedString = (string) => string.charAt(0).toUpperCase() + string.slice(1)

export default function Block({ block }) {
	const properties = Object.keys(block)
	return (
		<ul className='w-80'>
			{properties.map((property, index) => (
				<li key={index} className='break-words'>
					{capitalizedString(property).replace(/_/g, ' ') + `: ${block[property]}`}
				</li>
			))}
		</ul>
	)
}
