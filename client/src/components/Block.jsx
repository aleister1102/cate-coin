import React, { useEffect, useState } from 'react'
import CopyButton from './CopyButton'
import classNames from 'classnames'

const capitalizeString = (string) =>
	string.charAt(0).toUpperCase() + string.slice(1)

export default function Block({ block }) {
	const { transactions, ...properties } = block
    
	const headerFields = Object.entries(properties).map(([key, value]) => (
		<li
			key={key}
			className='flex justify-between'>
			<span className='font-medium'>{capitalizeString(key.replace(/_/g, ' '))}</span>
			<span className='w-56 text-end truncate'>{value}</span>
		</li>
	))

	const transactionFields = transactions.map((transaction, key) => (
		<li
			key={key}
			className='text-center'>
			{' '}
			{transaction}{' '}
		</li>
	))

	return (
		<div className='w-96 h-96 p-4 border-2 border-primary rounded-xl flex flex-col items-center justify-between shadow-sm shadow-gray-300'>
			<ul className='w-full'>{headerFields}</ul>
			<div
				className={classNames({
					'border-2 border-primary rounded-md w-full p-4':
                    transactions.length,
				})}>
				<ul className='w-full'>{transactionFields}</ul>
			</div>
			<CopyButton text={properties.hash} />
		</div>
	)
}
