import { Link } from 'react-router-dom'
import Tooltip from './Tooltip'
import { useState } from 'react'

export default function Header({ blockchain }) {
	const links = [
		{ text: 'Blockchain', path: '/' },
		{ text: 'Add transactions', path: '/add-transactions' },
		{ text: 'Transactions queue', path: '/transactions-queue' },
		{ text: 'Mine block', path: '/mine-block' }
	]

	const { length, difficulty, reward } = blockchain
	const [showTooltip, setShowTooltip] = useState(false)

	return (
		<div className='h-24 flex bg-primary shadow-md fixed w-full top-0'>
			<img
				src='https://s3.coinmarketcap.com/static/img/portraits/627c1542e20b3404341cde7d.png'
				alt='logo'
				className='h-full w-24'
				onMouseEnter={() => setShowTooltip(true)}
				onMouseLeave={() => setShowTooltip(false)}
			/>
			<ul className='h-full flex justify-start items-center gap-4 ml-4'>
				{links.map(({ text, path }, index) => (
					<li
						className='text-xl font-bold uppercase p-4 text-white'
						key={index}>
						<Link to={path}>{text}</Link>
					</li>
				))}
			</ul>
			{showTooltip && <Tooltip
				text={`Length: ${length}; Difficulty: ${difficulty}; Reward: ${reward}`}
			/>}
		</div>
	)
}
